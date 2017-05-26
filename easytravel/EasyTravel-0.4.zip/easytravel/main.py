from skyscanner.skyscanner import Flights
from easytravel.Structures import *
from easytravel.arrays import *
import pygame
from urllib.request import urlopen
import io
from json import loads
from webbrowser import open_new_tab

# DO NOT CHANGE api_key OR ENTER A VALID ONE
api_key = 'uc817271155344762646981250767433'

flights_service = Flights(api_key)
currency = 'UAH'


def main():
    (originplace, destinationplace, outbounddate, inbounddate, adults, children, money) = get_flight_info()
    people = adults+children

    result = flights_service.get_result(
        country='UK',
        currency=currency,
        locale='uk-UA',
        originplace=originplace+'-sky',
        destinationplace=destinationplace+'-sky',
        outbounddate=outbounddate,
        inbounddate=inbounddate,
        adults=adults,
        children=children).parsed

    result = eval(str(result))
    agents = Agents([Agent(el['Id'], el['Name'], el['ImageUrl']) for el in result['Agents']])
    places = Places([Place(el['Id'], el['Code'], (el['ParentId'] if 'ParentId' in el else 0))
                     for el in result['Places']], api_key)
    legs = Legs([Leg(el['Id'], el['FlightNumbers'][0]['FlightNumber'],
                     el['OriginStation'], el['DestinationStation'], places)
                 for el in result['Legs']])

    flights = [Flight(el['PricingOptions'][0]['Price'], currency, people, el['PricingOptions'][0]['DeeplinkUrl'],
                      agents.by_id(el['PricingOptions'][0]['Agents'][0]), legs.by_id(el['OutboundLegId']))
               for el in result['Itineraries'] if el['PricingOptions'][0]['Price'] <= money/people]

    Data = DynamicArray()
    for flight in flights:
        Data.append(flight)

    pygame.init()

    max_length = 10
    start_count = 0
    max_start = len(Data)-10

    screen = pygame.display.set_mode((900, 600))
    caption = outbounddate + ' | ' + originplace + ' - ' + destinationplace + ' |'
    pygame.display.set_caption(caption)

    update_screen(screen, Data, start_count, max_length, 'link_box.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    start_count += 1
                    if start_count > max_start:
                        start_count = max_start
                        break

                elif event.key == pygame.K_UP:
                    start_count -= 1
                    if start_count < 0:
                        start_count = 0
                        break

                update_screen(screen, Data, start_count, max_length, 'easytravel/resources/link_box.png')
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if 850 <= position[0] <= 850+40:
                    for i in range(max_length):
                        if 15+60*i <= position[1] <= 15 + 34 + 60*i:
                            lynk = Data.__getitem__(i+start_count).__getitem__(2)
                            open_new_tab(lynk)


def get_flight_info():
    place_check_url = 'https://www.skyscanner.net/dataservices/geo/v2.0/autosuggest/UK/en-GB/'
    while True:
        try:
            origin_place = input("Enter origin place: ")
            origin_place = loads(urlopen(place_check_url+origin_place).read().decode('utf8'))[0]['PlaceId']
            break
        except:
            pass

    while True:
        try:
            destination_place = input("Enter destination place: ")
            destination_place = loads(urlopen(place_check_url+destination_place).read().decode('utf8'))[0]['PlaceId']
            break
        except:
            pass

    outbound_date = input('Enter outbound date as yyyy-mm-dd: ')
    inbound_date = input('Enter inbound date as yyyy-mm-dd or Enter for one-way fligth: ')

    amount_adults = int(input('Enter number of adults(1-8): '))
    assert 1 <= amount_adults <= 8, "Incorect value"

    amount_children = int(input('Enter number of children(0-8): '))
    assert 0 <= amount_children <= 8, "Incorect value"

    budget = int(input('Enter your budget: '))
    return origin_place, destination_place, outbound_date, inbound_date, amount_adults, amount_children, budget


def update_screen(screen, data, start, max_length, link_image):
    screen.fill((255, 255, 255))

    for i in range(max_length):
        try:
            current_array = data.__getitem__(i+start)
        except:
            break
        link = current_array.__getitem__(0)
        image_str = urlopen(link).read()
        image_file = io.BytesIO(image_str)
        image = pygame.image.load(image_file)
        image = pygame.transform.scale(image, (100, 50))
        pygame.draw.rect(screen, (0, 0, 0), (19, 4+60*i, 102, 52))

        screen.blit(image, (20, 5+60*i))
        font = pygame.font.SysFont('Arial', 20)
        screen.blit(font.render(current_array[1], True, (0, 0, 0)), (125, 15+60*i))

        link_box = pygame.image.load(link_image)
        link_box = pygame.transform.scale(link_box, (40, 34))
        screen.blit(link_box, (850, 8+60*i))
    pygame.display.flip()
