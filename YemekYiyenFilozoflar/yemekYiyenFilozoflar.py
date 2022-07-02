import random
import time
from threading import Thread, Semaphore       #aynı zaman içerisinde birden fazla işlemin yapılmasını sağlar

class yemekYiyenFilozoflar(Thread):

    def __init__(self, *args, **kwargs):  #gelen filozofları ve çatalları aldık
        self.index = kwargs.pop("index")
        self.forks = kwargs.pop("forks")
        self.multiplex = kwargs.pop("multiplex")

        super(yemekYiyenFilozoflar, self).__init__(*args, **kwargs)

    @property
    def sol(self):              #Filozofların sol taraftaki catallarının indexlerinin belirliyoruz. Bunuda filozofun
        return self.index % 5   #index numarasıyla yapıyoruz filozofların indexlerinin mod 5 alınarak soltaraflarındaki
                                #çatalın yerinin bulmuş oluruz.

    @property
    def sag(self):                    #filozofların indexlerinin kullanarak filozofun sol tarafındaki erişebileceği catalın
        return (self.index + 1) % 5   #index'ini bulabiliyoruz bunuda filozofun index ini bir artırdıktan sonra modunu alarak bulabiliriz.

    def bekle(self):                  #çatal alamayan filozofları bekletiyoruz.
        time.sleep(0.1)

    def catallar(self):#ÇATALLAR
        self.multiplex.acquire()
        self.forks[self.sol].acquire()#SOL ÇATALI AL filozof un sol çatalı aldıktan sonra başka filozofların almasına izin vermeyerek
        print ("{} sol çatalı aldı {}\n".format(self.index, self.sol))#filozofun işi bitene kadar bekletiyor.
        self.forks[self.sag].acquire()#SAĞ ÇATALI AL # filozofun sag çatalı almasıyla birlikte başka filozofun sag catalı almamasına
        print("{} sağ çatalı aldı {}\n".format(self.index, self.sag))#filozofun çatalla işini bitene bakleyecektirler.
        # print lerin içinde ise filozofun ve hangi çatalı aldığını yazmasını sağlıyor

    def yemek(self):# filozofun sag ve sol çatalı almasıyla birlikte yemek yediğini belirtecek olan metod
        print("{} yemek yiyor. Afiyet Olsun\n".format(self.index))
        time.sleep(random.random())

    def catalıBırak(self):#ÇATALI BIRAK
        self.forks[self.sol].release()#filozofların sol catalı bıraktığını
        print( "{} Sol çatalı bıraktı {}\n".format(self.index, self.sol))
        self.forks[self.sag].release()#filozofların sağ çatalı bıraktığını
        print("{} sağ çatalı bıraktı {}\n".format(self.index, self.sag))
        self.multiplex.release()


    def run(self):
        dön=50
        while dön>=10:#filozofların yemek yemesi için masada kaç kere dönmesi gerektiğini belirtiyor isteğe bağlı olarak değişebiliriz.
            self.bekle()
            self.catallar()#filozofların çatalları almasıyla birlikte her iki çatalı alan filozofun
            self.yemek()  #yemek yediğini alamayanların
            self.catalıBırak() # çatalları bırakması gerektiğini ve yemek yiyen filozofların da çatalları bırakması gerektiği
            time.sleep(0.1)
            dön=dön-1


def main():

    forks = [Semaphore(1) for i in range(5)]#kilitlenmeyi önlemek iiçin semaphore kullandık kırıtik bölge doluyken başka birinin gelmesini engelledik beklettik
    multiplex = Semaphore(4)# aynı anda birden fazla işlemin gelmsi
    for i in range(5): #5 filozof için döngüye soktuk
        yemekYiyenFilozoflar(index=i, forks=forks ,multiplex=multiplex).start()#filozoflaı ve çatalları gönderdik


if __name__ == '__main__':
    main()#çalıştırdık