import os
import gzip
import logging

log = logging.getLogger(__name__)


def get_files(dir: str):
    '''
    Функция предназначена для получения всех файлов из дирректории без рекурсивного обхода
    :param dir:
    :return:
    '''
    files = os.listdir(dir)
    log.debug(f'dir {dir}, list dir: {files}')
    files = [i for i in files if not os.path.isdir(os.path.join(dir, i))]
    log.info(f'{files}')
    return files


def unzip_and_delete(files: list, zipFIlesDir, dirResult):
    '''
    Фукция предназначена для распаковки файлов архивов
    :param files: наименование файлов которые необходимо разархивировать
    :param zipFIlesDir: директория где расположены файла для распаковки
    :param dirResult: директория куда необходимо распаковывать
    :return:
    '''
    for file in files:
        if str(file).endswith('.gz'):
            file_to_unzip = os.path.join(zipFIlesDir, file)
            file_to_write = os.path.join(dirResult, file.replace('.gz', ''))
            with gzip.open(file_to_unzip, 'rb') as f, \
                    open(file_to_write, 'wb') as f_out:
                f_out.write(f.read())
                log.info(
                    f'file: {file_to_unzip} was unziped and writed to {file_to_write}')

            # os.remove(file_to_unzip)
            # log.info(f'file {file_to_unzip} was removed')


def unzip(files: list, zipFIlesDir, dirResult):
    pass


if __name__ == '__main__':
    test = './test'
    resultdir = './result'
    logging.basicConfig(level=logging.INFO)
    # unzip_and_delete(
    get_files(test)
