from abc import ABC, abstractmethod

class abstract_model(ABC):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def predict(self, X):
        # X should be in the format of [["2020-06-21 12:15:17",3526826139003047,"fraud_Johnston-Casper","travel",3.19,"Falmouth","Furniture designer","1955-07-06"],
        #                               ["2020-06-21 12:18:27",4988304376504,"fraud_Bechtelar-Rippin","food_dining",7.93,"Rock Tavern","Building surveyor","1937-03-172"]]
        #                                                                                                                          
        pass
    
    @abstractmethod
    def retrain(self, X):
        # X should be in the format of [["2020-06-21 12:15:17",3526826139003047,"fraud_Johnston-Casper","travel",3.19,"Falmouth","Furniture designer","1955-07-06", 1],
        #                               ["2020-06-21 12:18:27",4988304376504,"fraud_Bechtelar-Rippin","food_dining",7.93,"Rock Tavern","Building surveyor","1937-03-172", 0]]
        # 
        # where the last is either a 0 or 1, representing non-anomaly or anomaly respectively
        pass