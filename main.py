import random
import threading
from time import sleep
import copy

taxi_list = []
taxi_history = {}


class Taxi:
    def __init__(self, taxi_id, current_location='A', earnings=0):
        self.taxi_id = taxi_id
        self.raid_id = ''
        self.current_location = current_location  # current_location is a character
        self.earnings = earnings
        self.fare = 0
        self.customer_id = ''
        self.is_allocated = False
        self.drop_time = 0
        self.pickup_time = 0
        self.drop_point = ''
        self.pickup_point = ''
        self.distance = 0

    def new_raid(self, customer_id, pickup_point, drop_point, pickup_time):
        self.pickup_point = pickup_point
        self.drop_point = drop_point
        self.distance = abs(ord(self.pickup_point) - ord(self.drop_point)) * 15
        self.customer_id = customer_id
        self.raid_id = self.taxi_id + '-' + str(random.randint(100000, 999999))
        self.pickup_time = int(pickup_time)
        self.drop_time = self.pickup_time + self.distance // 15
        self.is_allocated = True
        self.fare = self.__earnings_calculator(self.distance)
        self.earnings += self.fare

        # Start a new thread for raid completion
        t1 = threading.Thread(target=self.raid_completion)
        t1.start()

    def raid_completion(self):
        sleep_time = (self.distance // 15) * 60
        sleep(sleep_time)
        self.is_allocated = False
        self.current_location = self.drop_point
        self.raid_id = 0

    def __earnings_calculator(self, distance):
        return 100 + (distance - 5) * 10

    def cancel_raid(self):
        if self.is_allocated:
            self.is_allocated = False
            self.raid_id = ''
            self.earnings -= self.fare
            print(f"Raid with ID {self.raid_id} has been cancelled.")
        else:
            print("No raid to cancel.")
        print()



class TaxiBookingSystem:
    def __init__(self):
        for i in range(4):
            taxi_list.append(Taxi(f'taxi-{i + 1}'))

    def nearest_taxi(self, curr_location) -> Taxi:
        nearest_taxi = None
        min_distance = float('inf')
        min_earnings = float('inf')
        for taxi in taxi_list:
            if not taxi.is_allocated:
                curr_dis = abs(ord(taxi.current_location) - ord(curr_location))
                if curr_dis < min_distance or (curr_dis == min_distance and taxi.earnings < min_earnings):
                    min_distance = curr_dis
                    min_earnings = taxi.earnings
                    nearest_taxi = taxi
        return nearest_taxi

    def book_taxi(self, customer_id, pickup_point, drop_point, pickup_time):
        taxi = self.nearest_taxi(pickup_point)

        if taxi:
            # Save the state before the change for history

            taxi.new_raid(customer_id, pickup_point, drop_point, pickup_time)
            if taxi_history.get(taxi.taxi_id):
                taxi_history.get(taxi.taxi_id).append(copy.deepcopy(taxi))
            else:
                taxi_history[taxi.taxi_id] = [copy.deepcopy(taxi)]

            print(f"{taxi.taxi_id} is allocated and will reach you on time")
            print(f"{taxi.raid_id} is your trip id")
            print(f"Your calculated fare will {taxi.fare}")

            return
        print("Taxi is not allocated. Try after some time")

    def cancel_raid(self, raid_id):
        taxi_id = raid_id.split('-')

        raid_list = taxi_history.get(taxi_id[0]+'-'+taxi_id[1])
        if raid_list:
            for raid in raid_list:
                if raid.raid_id == raid_id:
                    raid.cancel_raid()
                    return
        else:
            print("No raid is found with the given raid_id")

def location_checker(location):
    if len(location) == 1 and ord('A') <= ord(location) <= ord('E'):
        return True
    print()
    print('enter valid location')
    print()
    return False


if __name__ == '__main__':
    print("Welcome to Taxi booking system")

    taxi_booking_system = TaxiBookingSystem()

    while True:
        print("Enter 1 to book a taxi")
        print("Enter 2 to cancel a raid")
        print("Enter 3 to exit")

        try:
            choice = int(input().strip())
        except ValueError:
            print()
            print("Please enter a valid choice.")
            print()
            continue

        if choice == 1:
            customer_id = input("Enter your id: ").strip()
            pickup_point = input("Enter your pickup point: ").strip().upper()

            if not location_checker(pickup_point):
                continue

            drop_point = input("Enter your drop point: ").strip().upper()

            if not location_checker(drop_point):
                continue

            try:
                pickup_time = int(input("Enter your pickup time: ").strip())
            except ValueError:
                print()
                print("Please enter a valid pickup time.")
                print()
                continue

            print()
            taxi_booking_system.book_taxi(customer_id, pickup_point, drop_point, pickup_time)
            print()

        elif choice == 2:
            raid_id = input('Enter your raid id: ').strip()
            taxi_booking_system.cancel_raid(raid_id)

        elif choice == 2:
            print("\nThanks for using")
            exit(0)