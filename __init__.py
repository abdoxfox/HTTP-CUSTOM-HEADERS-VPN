from src.tunnel import Tun
class injector_init_():
    def __init__(self):
        self.Tun = Tun()
    def main(self):
        self.Tun.create_connection()
        
        
     
if __name__=="__main__":
    run= injector_init_()
    run.main()
       
       
