from os import path, access, R_OK

from scoretuple import ScoreTuple


class ScoreStorage:

    @staticmethod
    def create_in_storage(mem):
        ScoreStorage.write_to_storage(mem)

    @staticmethod
    def write_to_storage(mem):
        sco_file = ScoreStorage.__get_score_file()
        bw = open(sco_file, 'w')
        scoreinit = mem.scoreinit
        scorehigh = mem.scorehigh
        for i in range(10):
            bw.write(scoreinit[i + 1])
            bw.write('\n')
            bw.write(str(scorehigh[i + 2]))
            bw.write('\n')
        bw.flush()
        bw.close()

    @staticmethod
    def __get_score_file():
        file_name = "../digger.sco"
        file_path = path.abspath(file_name)
        return file_path

    @staticmethod
    def read_from_storage(mem):
        sco_file = ScoreStorage.__get_score_file()
        if not path.isfile(sco_file) or not access(sco_file, R_OK):
            return False
        br = open(sco_file, 'r')
        sc = [None for _ in range(10)]
        for i in range(10):
            name = br.readline().strip()
            score = int(br.readline().strip())
            sc[i] = ScoreTuple(name, score)
        br.close()
        mem.scores = sc
        return True
