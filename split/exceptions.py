
class AmountSumMismatchError(Exception):
    
    def __init__(self, message="Amount sum is not equal"):
        self.message = message
        super().__init__(self.message)