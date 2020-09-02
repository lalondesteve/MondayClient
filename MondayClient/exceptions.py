class MondayAPIError(RuntimeError):
    def __init__(self, monday_error, *args, **kwargs):
        self.error_code = monday_error['error_code']
        self.message = monday_error['error_message']
        msg = f'{self.error_code} - {self.message}'
        super().__init__(msg, *args, **kwargs)
