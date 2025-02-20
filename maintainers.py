import os

import psycopg2 as ps2
from telethon import TelegramClient
from telethon import connection as tel_connection
from telethon import events, sync


def send_result(best_flights, request_data):
    """Отправляет данные о самом дешевом рейсе в Телеграм"""
    if not best_flights:
        with TelegramClient(
            "flight_catcher", int(os.getenv("TELEGRAM_API")), os.getenv("TELEGRAM_HASH")
        ) as client:
            client.send_message(
                request_data["telegr_acc"],
                message=f'Перелет {request_data["depart_city"]} - {request_data["dest_city"]} на дату '
                f'{request_data["depart_date"]} не найден. Измените дату или условия поиска',
            )
        return False

    if isinstance(best_flights[0], dict):
        for i in range(len(best_flights)):
            if best_flights[i]["num_tranship"] == 0:
                with TelegramClient(
                    "flight_catcher",
                    int(os.getenv("TELEGRAM_API")),
                    os.getenv("TELEGRAM_HASH"),
                ) as client:
                    client.send_message(
                        request_data["telegr_acc"],
                        message=f'Перелет {best_flights[i]["orig_city"]} - {best_flights[i]["dest_city"]} цена {best_flights[i]["price"]} руб.: \nавиакомпания {best_flights[i]["carrier"]} рейс № {best_flights[i]["flight_number"]}\nвылет: {best_flights[i]["depart_date_time"]} прибытие: {best_flights[i]["arrive_date_time"]}\nпродолжительность {(best_flights[i]["total_flight_time"]) // 60} ч. {(best_flights[i]["total_flight_time"]) % 60} мин.',
                    )
            else:
                with TelegramClient(
                    "flight_catcher",
                    int(os.getenv("TELEGRAM_API")),
                    os.getenv("TELEGRAM_HASH"),
                ) as client:
                    client.send_message(
                        request_data["telegr_acc"],
                        message=f'Перелет {best_flights[i]["orig_city"]} - {best_flights[i]["dest_city"]} цена {best_flights[i]["price"]} руб.: \nавиакомпания {best_flights[i]["carrier"]} рейс № {best_flights[i]["flight_number"]}\nвылет: {best_flights[i]["depart_date_time"]} прибытие: {best_flights[i]["arrive_date_time"]} пересадки: {str(*best_flights[i]["tranship_cities"])}\nпродолжительность {(best_flights[i]["total_flight_time"]) // 60} ч. {(best_flights[i]["total_flight_time"]) % 60} мин.',
                    )
    elif isinstance(best_flights[0], list):
        for i in range(len(best_flights)):
            with TelegramClient(
                "flight_catcher",
                int(os.getenv("TELEGRAM_API")),
                os.getenv("TELEGRAM_HASH"),
            ) as client:
                client.send_message(
                    request_data["telegr_acc"],
                    message=f'Перелет {best_flights[i][0]["orig_city"]} - {best_flights[i][0]["dest_city"]} - {best_flights[i][0]["orig_city"]} цена {best_flights[i][0]["price"]} руб.:\nТуда:\nавиакомпания {best_flights[i][0]["carrier"]} рейс № {best_flights[i][0]["flight_number"]}\nвылет: {best_flights[i][0]["depart_date_time"]} прибытие: {best_flights[i][0]["arrive_date_time"]} пересадки: {str(*best_flights[i][0]["tranship_cities"]) if best_flights[i][0]["num_tranship"] != 0 else "нет"}\nпродолжительность {(best_flights[i][0]["total_flight_time"]) // 60} ч. {(best_flights[i][0]["total_flight_time"]) % 60} мин.\nНазад:\nавиакомпания {best_flights[i][1]["carrier"]} рейс № {best_flights[i][1]["flight_number"]}\nвылет: {best_flights[i][1]["depart_date_time"]} прибытие: {best_flights[i][1]["arrive_date_time"]} пересадки: {str(*best_flights[i][1]["tranship_cities"]) if best_flights[i][1]["num_tranship"] != 0 else "нет"}\nпродолжительность {(best_flights[i][1]["total_flight_time"]) // 60} ч. {(best_flights[i][1]["total_flight_time"]) % 60} мин.',
                )
    return True


def set_connection():
    try:
        db_connection = ps2.connect(
            host=os.getenv("HOST"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB"),
            port=os.getenv("PORT"),
        )
        db_connection.autocommit = True
        return db_connection

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
        raise _ex
