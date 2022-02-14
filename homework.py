from dataclasses import asdict, dataclass, fields


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO_MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self):
        return(self.INFO_MESSAGE.format(**asdict(self)))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

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
    SPEED_MULTYPLIER = 18
    SPEED_CORRECTION_FACTOR = 20

    def get_spent_calories(self):
        return((
            self.SPEED_MULTYPLIER * self.get_mean_speed()
            - self.SPEED_CORRECTION_FACTOR)
            * self.weight / self.M_IN_KM * (self.duration * self.MIN_IN_H))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: int
    WEIGHT_MULTYPLIER_1 = 0.035
    WEIGHT_MULTYPLIER_2 = 0.029

    def get_spent_calories(self):
        return((self.WEIGHT_MULTYPLIER_1 * self.weight + (
            self.get_mean_speed() ** 2 // self.height)
            * self.WEIGHT_MULTYPLIER_2 * self.weight)
            * (self.duration * self.MIN_IN_H))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    SPEED_ADDITION = 1.1
    WEIGHT_MULTYPLIER = 2

    def get_distance(self):
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        return((self.get_mean_speed() + self.SPEED_ADDITION)
               * self.WEIGHT_MULTYPLIER * self.weight)


CODE_NAMES = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}
EXCEPTION_MESSAGE = (
    'Для тренировки {0} '
    'ожидали число параметров {1}, '
    'получили {2}'
)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if len(data) == len(fields(CODE_NAMES[workout_type])):
        return CODE_NAMES[workout_type](*data)
    else:
        raise ValueError(
            EXCEPTION_MESSAGE.format(
                workout_type,
                len(fields(CODE_NAMES[workout_type])),
                len(data))
        )


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
