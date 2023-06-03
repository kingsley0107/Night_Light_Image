# -*- coding: utf-8 -*-
"""
Created on 03 Jun 3:55 PM

@Author: kingsley leung
@Email: kingsleyl0107@gmail.com

_description_: file runner
"""
from config.static_vars import RESULT_PATH
from process.schedule import schedule


def main():
    result = schedule()

    result.to_csv(RESULT_PATH)


if __name__ == '__main__':
    main()
