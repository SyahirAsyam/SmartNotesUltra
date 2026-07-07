
import os
import shutil
import zipfile


def export_notes():

    export_folder = "Export"

    if not os.path.exists(export_folder):

        os.makedirs(export_folder)

    return export_folder

def copy_database(export_folder):

    files = [

        "notes.json",

        "settings.json",

        "folders.json",

        "favorites.json",

        "recycle_bin.json"

    ]

    for file in files:

        if os.path.exists(file):

            shutil.copy(

                file,

                export_folder
            )

def create_zip():

    export_folder = export_notes()

    copy_database(export_folder)

    zip_name = get_backup_name()

    shutil.make_archive(

        zip_name,

        "zip",

        export_folder

    )

    print(

        "Backup berhasil!",

        zip_name + ".zip"

    )

    return zip_name + ".zip"

def get_backup_name():

    number = 1

    while True:

        export_folder = "Export"

        if not os.path.exists(export_folder):

            os.makedirs(export_folder)

        filename = os.path.join(

            export_folder,

            f"UltraSmartNotes_Backup_{number:03}.zip"

        )

        if not os.path.exists(filename):

            return filename[:-4]

        number += 1

def import_backup(zip_path):

    temp_folder = "TempRestore"

    if os.path.exists(temp_folder):

        shutil.rmtree(temp_folder)

    os.makedirs(temp_folder)

    with zipfile.ZipFile(

        zip_path,

        "r"

    ) as zip_ref:

        zip_ref.extractall(

            temp_folder

        )

        restore_backup(

            temp_folder

        )

        print(

            "Restore selesai!"

        )

    print(

        "Backup berhasil diextract."

    )

    if os.path.exists(temp_folder):

        shutil.rmtree(temp_folder)

def restore_backup(temp_folder):

    files = [

        "notes.json",

        "settings.json",

        "folders.json",

        "favorites.json",

        "recycle_bin.json"

    ]

    for file in files:

        source = os.path.join(

            temp_folder,

            file

        )

        if os.path.exists(source):

            shutil.copy(

                source,

                file

            )