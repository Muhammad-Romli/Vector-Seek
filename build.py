from os_functions.file_operator import read_from, convert_file_dict_to_dict_metadata
from converter_functions.metadata_to_vector import metadata_to_vector

file_package = read_from() #if you dont want to use src_folder, just put the path of your folder relative to the root of project directory
if file_package == None:
    raise FileExistsError("There is no files inside src(or your own custom folder) folder maybe try adding some")
package_of_metadatas = convert_file_dict_to_dict_metadata(file_package)
metadata_to_vector(package_of_metadatas)