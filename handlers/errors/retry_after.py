from aiogram import exceptions
from loader import dp


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """

    # if isinstance(exception, exception.CantDemoteChatCreator):
    #     return True
    #
    if isinstance(exception, exceptions.MessageNotModified):
        return True
    # if isinstance(exception, exception.MessageCantBeDeleted):
    #     return True
    #
    # if isinstance(exception, exception.MessageToDeleteNotFound):
    #     return True
    #
    # if isinstance(exception, exception.MessageTextIsEmpty):
    #     return True
    #
    # if isinstance(exception, exception.Unauthorized):
    #     return True
    #
    # if isinstance(exception, exception.InvalidQueryID):
    #     return True
    #
    # # if isinstance(exception, exception.TelegramAPIError):
    #     return True

    if isinstance(exception, exceptions.RetryAfter):
        return True

    # if isinstance(exception, exception.CantParseEntities):
    #     return True
