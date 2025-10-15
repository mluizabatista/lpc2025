from core.core import printDoCore
from ship.ship import printDoShip   
from tank.tank import printDoTank

def main():

    core = printDoCore()
    ship = printDoShip()
    tank = printDoTank()

    core.print_do_core()
    ship.print_do_ship()
    tank.print_do_tank()

if __name__ == "__main__":
    main()