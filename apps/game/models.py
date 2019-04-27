from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django_mysql.models import JSONField

from apps.main.mixins import CreatedUpdatedMixin
from .logic import handle_field_test, handle_game_lose, \
    check_game_win, generate_field


class GameStatusEnum:
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    WIN = 'win'
    LOSE = 'lose'
    CHOICES = (
        (CREATED, 'Created'),
        (IN_PROGRESS, 'In progress'),
        (WIN, 'Win'),
        (LOSE, 'Lose'),
    )


# Current player's turn
class GameTurnEnum:
    FIRST = 'first'
    SECOND = 'second'
    CHOICES = (
        (FIRST, FIRST.title()),
        (SECOND, SECOND.title()),
    )


# Possible game field marks:
# '*' - mine
# ' ' - empty field
# 1-n - digit-indicator
# Every field is an array of 3 elements: [mark, visible_flag, flagged].
# ex: ['x', False, True] - disabled mine
class Game(CreatedUpdatedMixin):
    field = JSONField()
    field_size = models.IntegerField(
        default=8)
    rest_flags_count = models.IntegerField(
        default=10)
    status = models.CharField(
        max_length=15,
        choices=GameStatusEnum.CHOICES,
        default=GameStatusEnum.CREATED)
    current_turn = models.CharField(
        max_length=10,
        choices=GameTurnEnum.CHOICES,
        default=GameTurnEnum.FIRST)
    first_player = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True, null=True)
    second_player = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True, null=True)

    @classmethod
    def create_new_game(cls, player, size=8, mines=6, flags=8):
        return cls.objects.create(
            field=generate_field(size, mines),
            first_player=player,
            field_size=size,
            rest_flags_count=flags)

    def start_single_game(self):
        self.status = GameStatusEnum.IN_PROGRESS
        self.save()

    def join_game(self, player):
        self.second_player = player
        self.status = GameStatusEnum.IN_PROGRESS
        self.save()

    def test_field(self, position):
        """
        Left-click on field
        :param position: coordinates, ex: [1, 1]
        :return: None, PermissionDenied on error
        """
        try:
            x, y = position
            mark, visible, flagged = self.field[x][y]
            if visible or flagged:
                raise PermissionDenied('You are already opened or flagged this field')

            if mark == '*':
                self.status = GameStatusEnum.LOSE
                handle_game_lose(self.field, self.field_size)
            else:
                handle_field_test(self.field, x, y, self.field_size)

            if check_game_win(self.field, self.field_size):
                self.status = GameStatusEnum.WIN

            self.current_turn = self._get_next_turn()
            self.save()
        except (KeyError, ValueError):
            raise PermissionDenied('Bad position!')

    def flag_field(self, position):
        """
        Right-click on field
        :param position: coordinates, ex: [1, 1]
        :return: None
        """
        x, y = position
        self.field[x][y][2] = True
        if check_game_win(self.field, self.field_size):
            self.status = GameStatusEnum.WIN

        self.rest_flags_count -= 1
        self.current_turn = self._get_next_turn()
        self.save()

    def _get_next_turn(self):
        if self.current_turn == GameTurnEnum.FIRST:
            return GameTurnEnum.SECOND
        else:
            return GameTurnEnum.FIRST
