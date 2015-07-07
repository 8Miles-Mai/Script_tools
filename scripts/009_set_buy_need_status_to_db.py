#!/usr/local/bin/python


from gm_common import *


def flush_buy_need_status_to_db():
    update_bl_status_to_db()
    return True



if __name__ == "__main__":

    log("update buy need status as online by the data")
    flush_buy_need_status_to_db()



