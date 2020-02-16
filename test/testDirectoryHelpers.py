import unittest
from pathlib import Path
import shutil
import directoryHelpers as dh


class TestDirectoryHelpers(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDirectoryHelpers, self).__init__(*args, **kwargs)
        # create the following structure for tests:
        #
        # polygon/
        # ├── 1
        # ├── 2
        # ├── a /
        # │   ├── 3
        # │   ├── 4
        # │   └── c /
        # │       └── 5
        # └── b /
        #     ├── 6
        #     └── d /
        self.not_existing = Path("./thisDirectoryIsMostLikelyNotExistingHere")
        self.root = Path("./polygon")
        self.f_1 = self.root / "1"
        self.f_2 = self.root / "2"

        self.d_a = self.root / "a"
        self.f_3 = self.d_a / "3"
        self.f_4 = self.d_a / "4"

        self.d_c = self.d_a / "c"
        self.f_5 = self.d_c / "5"

        self.d_b = self.root / "b"
        self.f_6 = self.d_b / "6"
        self.d_d = self.d_b / "d"

        self.polygon_dirs = [self.root, self.d_a, self.d_b, self.d_c, self.d_d]
        self.polygon_files = [self.f_1, self.f_2, self.f_3, self.f_4, self.f_5, self.f_6]

    def setUp(self) -> None:
        if self.not_existing.exists():
            shutil.rmtree(str(self.not_existing))

        if self.root.exists():
            shutil.rmtree(str(self.root))

        for dir in self.polygon_dirs:
            dir.mkdir(parents=True, exist_ok=False)

        for file in self.polygon_files:
            file.touch(exist_ok=False)

    def tearDown(self) -> None:
        if self.root.exists():
            shutil.rmtree(str(self.root))

    def test_is_existing_dir(self):
        self.assertTrue(dh.is_existing_directory(self.root))
        self.assertFalse(dh.is_existing_directory(self.f_1))
        self.assertFalse(dh.is_existing_directory(self.not_existing))

    def test_ensure_is_existing_dir(self):
        self.assertRaises(NotADirectoryError, dh.ensure_is_existing_directory, self.not_existing)
        self.assertRaises(NotADirectoryError, dh.ensure_is_existing_directory, self.f_1)

        try:
            dh.ensure_is_existing_directory(self.root)
        except:
            self.fail("ensure_is_existing_directory() should not raise here!")

    def test_list_only_dirs(self):
        dirs = dh.list_only_dirs(self.root)
        self.assertEqual(len(dirs), 2)
        self.assertIn(self.d_a, dirs)
        self.assertIn(self.d_b, dirs)

        dirs = dh.list_only_dirs(self.d_a)
        self.assertEqual(len(dirs), 1)
        self.assertIn(self.d_c, dirs)

        dirs = dh.list_only_dirs(self.d_c)
        self.assertEqual(len(dirs), 0)

        self.assertRaises(NotADirectoryError, dh.list_only_dirs, self.f_1)

    def test_list_only_files(self):
        fls = dh.list_only_files(self.root)
        self.assertEqual(len(fls), 2)
        self.assertIn(self.f_1, fls)
        self.assertIn(self.f_2, fls)

        fls = dh.list_only_files(self.d_a)
        self.assertEqual(len(fls), 2)
        self.assertIn(self.f_3, fls)
        self.assertIn(self.f_4, fls)

        fls = dh.list_only_files(self.d_c)
        self.assertEqual(len(fls), 1)
        self.assertIn(self.f_5, fls)

        fls = dh.list_only_files(self.d_b)
        self.assertEqual(len(fls), 1)
        self.assertIn(self.f_6, fls)

        fls = dh.list_only_files(self.d_d)
        self.assertEqual(len(fls), 0)

        self.assertRaises(NotADirectoryError, dh.list_only_files, self.not_existing)
        self.assertRaises(NotADirectoryError, dh.list_only_files, self.f_1)

    def test_list_content(self):
        all = dh.list_content(self.root)
        self.assertEqual(len(all), 4)
        self.assertIn(self.f_1, all)
        self.assertIn(self.f_2, all)
        self.assertIn(self.d_a, all)
        self.assertIn(self.d_b, all)

        all = dh.list_content(self.d_a)
        self.assertEqual(len(all), 3)
        self.assertIn(self.f_3, all)
        self.assertIn(self.f_4, all)
        self.assertIn(self.d_c, all)

        all = dh.list_content(self.d_c)
        self.assertEqual(len(all), 1)
        self.assertIn(self.f_5, all)

        all = dh.list_content(self.d_d)
        self.assertEqual(len(all), 0)

        self.assertRaises(NotADirectoryError, dh.list_content, self.not_existing)
        self.assertRaises(NotADirectoryError, dh.list_content, self.f_6)

    def test_list_dirs_recursively(self):
        dirs = dh.list_dirs_recursively(self.root)
        self.assertEqual(len(dirs), 4)
        self.assertIn(self.d_a, dirs)
        self.assertIn(self.d_b, dirs)
        self.assertIn(self.d_c, dirs)
        self.assertIn(self.d_d, dirs)

        dirs = dh.list_dirs_recursively(self.d_a)
        self.assertEqual(len(dirs), 1)
        self.assertIn(self.d_c, dirs)

        dirs = dh.list_dirs_recursively(self.d_d)
        self.assertEqual(len(dirs), 0)

        self.assertRaises(NotADirectoryError, dh.list_dirs_recursively, self.f_1)

    def test_list_files_recursively(self):
        fls = dh.list_files_recursively(self.root)
        self.assertEqual(len(fls), 6)
        for file in self.polygon_files:
            self.assertIn(file, fls)

        fls = dh.list_files_recursively(self.d_c)
        self.assertEqual(len(fls), 1)
        self.assertIn(self.f_5, fls)

        fls = dh.list_files_recursively(self.d_d)
        self.assertEqual(len(fls), 0)

        self.assertRaises(NotADirectoryError, dh.list_files_recursively, self.not_existing)
        self.assertRaises(NotADirectoryError, dh.list_files_recursively, self.f_6)

    def test_list_all_dir_content_recursively(self):
        all = dh.list_all_dir_content_recursively(self.root)
        self.assertEqual(len(all), 10)
        for file in self.polygon_files:
            self.assertIn(file, all)

        for dir in self.polygon_dirs:
            if dir != self.root:
                self.assertIn(dir, all)

        all = dh.list_all_dir_content_recursively(self.d_b)
        self.assertEqual(len(all), 2)
        self.assertIn(self.d_d, all)
        self.assertIn(self.f_6, all)

        all = dh.list_all_dir_content_recursively(self.d_c)
        self.assertEqual(len(all), 1)
        self.assertIn(self.f_5, all)

        all = dh.list_all_dir_content_recursively(self.d_d)
        self.assertEqual(len(all), 0)

        self.assertRaises(NotADirectoryError, dh.list_all_dir_content_recursively, self.not_existing)
        self.assertRaises(NotADirectoryError, dh.list_all_dir_content_recursively, self.f_6)

    def test_move_all_files_1(self):
        dh.move_all_files(self.root, self.d_d)

        root_files = dh.list_only_files(self.root)
        d_files = dh.list_only_files(self.d_d)

        self.assertEqual(len(root_files), 0)

        self.assertEqual(len(d_files), 2)
        self.assertIn(self.d_d / self.f_1.name, d_files)
        self.assertIn(self.d_d / self.f_2.name, d_files)

    def test_move_all_files_2(self):
        dh.move_all_files(self.d_a, self.root)

        a_files = dh.list_files_recursively(self.d_a)
        self.assertEqual(len(a_files), 1)
        self.assertIn(self.f_5, a_files)

        root_files = dh.list_only_files(self.root)
        self.assertEqual(len(root_files), 4)
        self.assertIn(self.f_1, root_files)
        self.assertIn(self.f_2, root_files)
        self.assertIn(self.root / self.f_3.name, root_files)
        self.assertIn(self.root / self.f_4.name, root_files)

    def test_move_all_files_3(self):
        dir_1 = Path("asdf")
        dir_2 = Path("ghi")
        target = self.root / dir_1 / dir_2
        dh.move_all_files(self.root, target)

        root_files = dh.list_only_files(self.root)
        self.assertEqual(len(root_files), 0)

        files_in_asdf = dh.list_only_files(self.root / dir_1)
        self.assertEqual(len(files_in_asdf), 0)

        self.assertTrue(dh.is_existing_directory(target))
        target_files = dh.list_only_files(target)
        self.assertEqual(len(target_files), 2)
        self.assertIn(target / self.f_1.name, target_files)
        self.assertIn(target / self.f_2.name, target_files)

    def test_move_all_files_4(self):
        dh.move_all_files(self.d_d, self.root)

        root_files = dh.list_only_files(self.root)
        d_files = dh.list_only_files(self.d_d)

        self.assertEqual(len(root_files), 2)

        self.assertEqual(len(d_files), 0)
        self.assertIn(self.f_1, root_files)
        self.assertIn(self.f_2, root_files)

    def test_move_all_files_5(self):
        dh.move_all_files(self.root, self.root)

        root_files = dh.list_only_files(self.root)

        self.assertEqual(len(root_files), 2)

        self.assertIn(self.f_1, root_files)
        self.assertIn(self.f_2, root_files)

    def test_move_all_content_1(self):
        dh.move_all_content(self.d_a, self.d_b)

        a_content = dh.list_all_dir_content_recursively(self.d_a)
        self.assertEqual(len(a_content), 0)

        b_content = dh.list_all_dir_content_recursively(self.d_b)
        self.assertEqual(len(b_content), 2 + 4)

        self.assertIn(self.f_6, b_content)
        self.assertIn(self.d_d, b_content)
        self.assertIn(self.d_b / self.f_3.relative_to(self.d_a), b_content)
        self.assertIn(self.d_b / self.f_4.relative_to(self.d_a), b_content)
        self.assertIn(self.d_b / self.d_c.relative_to(self.d_a), b_content)
        self.assertIn(self.d_b / self.f_5.relative_to(self.d_a), b_content)





# create the following structure for tests:
#
# polygon/
# ├── 1
# ├── 2
# ├── a /
# │   ├── 3
# │   ├── 4
# │   └── c /
# │       └── 5
# └── b /
#     ├── 6
#     └── d /



