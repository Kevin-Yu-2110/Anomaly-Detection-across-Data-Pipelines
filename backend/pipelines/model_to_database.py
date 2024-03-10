import luigi

class SaveDummyOutput(luigi.Task):

    def output(self):
        return luigi.LocalTarget("dummy_output/dummy_output.csv")
    
    def run(self):
        with self.output().open("w") as f:
            f.write("1, 2, 3")
            f.close()