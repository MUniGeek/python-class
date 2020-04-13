"""Model for aircraft flights."""


class Flight:
    """ A flight with a particualar passenger aircraft."""
    
    def __init__(self, number, aircraft):
        if not number[:2].isalpha():
            raise ValueError(f"No airline code in '{number}'")
            
        if not number[:2].isupper():
            raise ValueError(f"Invalid airline code '{number}'")
            
        if not (number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError(f"Invalide route number '{number}'")
            
        self._number = number
        self._aircraft = aircraft
        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + [{letter: None for letter in seats} for _ in rows]
        
        
    def aircraft_model(self):
        """Returns aircraft model for this flight"""
        return self._aircraft.model()
    
    
    def number(self):
        """Reurns flight number"""
        return self._number
        
        
    def airline(self):
        """Returns airline code from flight number"""
        return self._number[:2]
        
        
    def allocate_seat(self, seat, passenger):
        """Allocate a seat to a passenger.
        
        Args:
            seat: a seat designator such as '12C' or '21F'.
            passenger: The passenger name.
            
        Raises:
            ValueError: if the seat is unavailable.
        """
        
        row, letter = self._parse_seat(seat)
            
        if self._seating[row][letter] is not None:
            raise ValueError(f"Seat {seat} already occupied")
            
        self._seating[row][letter] = passenger
        
        
    def relocate_passenger(self, from_seat, to_seat):
        """Relocate a passenger to a different seat.
        
        Args:
            from_seat: The existing seat designator for the 
                        passenger to be moved
                        
            to_seat: The new seat designator.
        """
        
        from_row, from_letter = self._parse_seat(from_seat)
        
        if self._seating[from_row][from_letter] is None:
            raise ValueError(f"No passenger to relocate in seat {from_seat}")
            
        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] is not None:
            raise ValueError(f"Seat {to_seat} alread occupied")
            
        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None
        
        
    def remove_passenger(self, seat):
        """Removes a passenger from a seat.
        
        Args:
            seat: seat to remove passenger from
        """
        
        row, letter = self._parse_seat(seat)
            
        if self._seating[row][letter] is None:
            raise ValueError(f"No passenger in {seat}")
            
        self._seating[row][letter] = None
        
        
    def num_available_seats(self):
        """Returns number of available seats on flight."""
        
        return sum(sum(1 for s in row.values() if s is None)
                    for row in self._seating
                    if row is not None)
                    
                    
    def return_seat(self, seat):
        """Returns name of passenger in specified seat
        
        Args:
            seat: a seat designator such as '12C' or '21F'.
            
        Raises:
            ValueError: if the seat is unavailable.
        """
        
        row, letter = self._parse_seat(seat)

        if self._seating[row][letter] is None:
            return "Empty"
        
        return self._seating[row][letter]
                    

    def find_passenger(self, passenger):
        """Finds passenger on plane and returns seat number.
        
        Args:
            passenger: Passenger name        
        """

        for seat, passenger_in in self._passenger_seats():
            if passenger_in == passenger:
                return seat
                
        return None
    
    
    def _parse_seat(self, seat):
        """Parses row and seat number from a seat number provided for other functions.
        For internal class use only.
        
        Args:
            seat: The seat to parse
        """
        
        rows, seat_letters = self._aircraft.seating_plan()
        
        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError(f"Invalid seat letter {letter}")
            
        row_text = seat[:-1]
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError(f"Invalid seat row {row_text}")
            
        if row not in rows:
            raise ValueError(f"Invalid row number {row}")
        
        return row, letter
        
        
    def make_boarding_cards(self, card_printer):
        """Creates borading cards for the card printer, and prints them using the specified card printer"""
        for seat, passenger in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.number(), self.aircraft_model())
            
    
    def _passenger_seats(self):
        """An iterable series of passenger seating locations."""
        row_numbers, seat_letters = self._aircraft.seating_plan()
        for row in row_numbers:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield (f"{row}{letter}", passenger)
                    
        


class Aircraft:

    def __init__(self, registration, model, num_rows, num_seats_per_row):
        self._registration = registration
        self._model = model
        self._num_rows = num_rows
        self._num_seats_per_row = num_seats_per_row
        
    def registration(self):
        """Returns aircraft registration"""
        return self._registration
        
    def model(self):
        """Returns aircraft model"""
        return self._model
        
    def seating_plan(self):
        """Returns seating plan as built by number of rows and number of seats"""
        return (range(1, self._num_rows + 1),
            "ABCDEFGHJK"[:self._num_seats_per_row])


def console_card_printer(passenger, seat, flight_number, aircraft):
    """Prints boarding cards passed by the flight's object
    
    Args:
        passenger: Passenger name
        seat: seat number
        flight_number: flight number
        aircraft: aircraft model
    """    
    
    output = f"| Name: {passenger}"         \
             f"  Seat: {seat}"              \
             f"  Flight: {flight_number}"   \
             f"  Aircraft: {aircraft}"      \
             " |"
    banner = "+" + "-" * (len(output) -2) + "+"
    border = "|" + " " * (len(output) -2) + "|"
    lines = [banner, border, output, border, banner]
    card = "\n".join(lines)
    print(card)
    print()
      

def test_flight():
    """Creates a test flight with the following details:
    
        Flight Number = BA758
        Aircraft Registration = "G-EUPT"
        Aircraft Model = Airbus A319
        Number of Rows = 22
        Number of seats per row = 6
    
    Seat Allocations:
        1A = Rob Mackenzie
        1C = Ava Mackenzie
        1D = Olivia Mackenzie
        1F = Krysta Mackenzie
        7A = Ashley Weinberger
        7B = Tytan Weinberger
        7C = Keirin Weinberger
        7D = Fat Guy 1
        7E = Travis Weinberger
        7F = Fat Guy 2 
    """
    
    f = Flight("BA758", Aircraft("G-EUPT", "Airbus A319", num_rows=22, num_seats_per_row=6))
    f.allocate_seat("1A", "Rob Mackenzie")
    f.allocate_seat("1C", "Ava Mackenzie")
    f.allocate_seat("1D", "Olivia Mackenzie")
    f.allocate_seat("1F", "Krysta Mackenzie")
    f.allocate_seat("7A", "Ashley Weinberger")
    f.allocate_seat("7B", "Tytan Weinberger")
    f.allocate_seat("7C", "Keirin Weinberger")
    f.allocate_seat("7D", "Fat Guy 1")
    f.allocate_seat("7E", "Travis Weinberger")
    f.allocate_seat("7F", "Fat Guy 2")
    
    return f