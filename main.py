import threading
import time
import random

# un Semaphore permite que se puedan "liberar" mas semaforos de los creados y con ello, se crean mas. En cambio, un BoundedSemaphore no permite eso.
semaphore = threading.BoundedSemaphore(1)
total_money: int = 1000

class CashRegister():
    def __init__(self, cash=100):
        self.cash = cash

    def add_money(self, qty):
        self.cash += qty

    def substract_money(self, qty):
        self.cash -= qty

    def restore_total_money(self):
        global total_money
        total_money += self.cash
        self.cash = 0

def make_cash_ops(register_number, *args):
    new_cash_register = CashRegister()

    for arg in args:
        qty = str(arg)
        
        if qty[0] == '-':
            new_cash_register.substract_money(-(arg))
            print(f"Caja #{register_number}: {str(new_cash_register.cash)}")
        else:
            new_cash_register.add_money(arg)
            print(f"Caja #{register_number}: {str(new_cash_register.cash)}")

    print(f"Caja #{register_number}, Dinero en caja: {new_cash_register.cash}")
    
    # Seccion critica.
    semaphore.acquire()
    new_cash_register.restore_total_money()
    time.sleep(5)
    semaphore.release()
    
    print(f"Dinero en tienda despues de caja #{register_number}: {str(total_money)}")

def main():    
    threads = []

    for i in range(5):
        ops_number: int = random.randint(1,5)
        arr = [random.randint(-100, 100) for _ in range(ops_number)]
        print(f"CAJA {i}, OPERACIONES: {arr}")

        thread = threading.Thread(target=make_cash_ops, args=(i, *arr))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"Dinero en tienda: {total_money}")

if __name__ == '__main__':
    main()