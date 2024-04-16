import pandas

df = pandas.read_csv("hotels.csv", dtype={"id": str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pandas.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, 'name'].squeeze()

    def book(self):
        df.loc[df["id"] == self.hotel_id, 'available'] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        availability = df.loc[df["id"] == self.hotel_id, 'available'].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel_object = hotel_object

    def generate(self):
        content = f"""Thank you for your reservation!
Here is you booking data:
Name: {self.customer_name}
Hotel: {self.hotel_object.name}"""
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number,
                     "expiration": expiration,
                     "cvc": cvc,
                     "holder": holder}
        if card_data in df_cards:
            return True


class SecureCreditCard(CreditCard):
    def authenticate(self, given_pass):
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_pass:
            return True


print(df)
hotel_id = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_id)
if hotel_id == "free all":
    # Hard reset for testing purposes
    df.loc[df['available'] == "no", "available"] = "yes"
    df.to_csv("hotels.csv", index=False)
elif hotel.available():
    credit_card = SecureCreditCard(number="1234567890123456")
    if credit_card.validate(expiration="01/99", holder="JOHN DOE", cvc="000"):
        if credit_card.authenticate(given_pass="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(name, hotel)
            print(reservation_ticket.generate())
        else:
            print("Password incorrect")
    else:
        print("There was a problem with your payment")
else:
    print("Hotel is not available")
