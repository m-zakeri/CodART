import os
import understand


class Metric:
    def __init__(self, udb_path):
        if not os.path.isfile(udb_path):
            raise ValueError("Project directory is not valid.")
        self.db = understand.open(udb_path)
        self.metrics = self.db.metric(self.db.metrics())

    @property
    def DSC(self):
        """
        DSC - Design Size in Classes
        :return: Total number of classes in the design.
        """
        return self.metrics.get('CountDeclClass', 0)

    @property
    def NOH(self):
        """
        NOH - Number Of Hierarchies
        count(MaxInheritanceTree(class)) = 0
        :return: Total number of 'root' classes in the design.
        """
        count = 0
        for ent in sorted(self.db.ents(kindstring='class'), key=lambda ent: ent.name()):
            if ent.kindname() == "Unknown Class":
                continue
            mit = ent.metric(['MaxInheritanceTree'])['MaxInheritanceTree']
            if mit == 1:
                count += 1
        return count

    @property
    def ANA(self):
        """
        ANA - Average Number of Ancestors
        :return: Average number of classes in the inheritance tree for each class
        """
        return None

    def print_all(self):
        for k, v in sorted(self.metrics.items()):
            print(k, "=", v)


if __name__ == '__main__':
    db_path = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    metric = Metric(db_path)
    # metric.print_all()
    print("DSC", metric.DSC)
    print("NOH", metric.NOH)

