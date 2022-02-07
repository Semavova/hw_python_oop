from dataclasses import dataclass, fields


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO_MESSAGE = (
        'Тип тренировки: {key_to_insert[0]}; '
        'Длительность: {key_to_insert[1]:.3f} ч.; '
        'Дистанция: {key_to_insert[2]:.3f} км; '
        'Ср. скорость: {key_to_insert[3]:.3f} км/ч; '
        'Потрачено ккал: {key_to_insert[4]:.3f}.'
    )

    def get_message(self):
        data = [
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories
        ]
        return self.INFO_MESSAGE.format(key_to_insert=data)


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000
    M_IN_H = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    action: int
    duration: float
    weight: float
    AVG_SPEED_MULTYPLIER = 18
    AVG_SPEED_CORRECTION_FACTOR = 20

    def get_spent_calories(self):
        spent_calories = ((
            self.AVG_SPEED_MULTYPLIER * self.get_mean_speed()
            - self.AVG_SPEED_CORRECTION_FACTOR)
            * self.weight / self.M_IN_KM * (self.duration * self.M_IN_H))
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration: float
    weight: float
    height: int
    WEIGHT_MULTYPLIER_1 = 0.035
    WEIGHT_MULTYPLIER_2 = 0.029

    def get_spent_calories(self):
        spent_calories = ((self.WEIGHT_MULTYPLIER_1 * self.weight + (
            self.get_mean_speed() ** 2 // self.height)
            * self.WEIGHT_MULTYPLIER_2 * self.weight)
            * (self.duration * self.M_IN_H))
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    AVG_SPEED_ADDITION = 1.1
    WEIGHT_MULTYPLIER = 2

    def get_distance(self):
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        spent_calories = ((self.get_mean_speed() + self.AVG_SPEED_ADDITION)
                          * self.WEIGHT_MULTYPLIER * self.weight)
        return spent_calories


CODENAMES = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if len(data) == len(fields(CODENAMES[workout_type])):
        return CODENAMES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
