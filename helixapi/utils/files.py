import base64
import json
import zlib
import binascii
import os

from enum import Enum
import time

class FileType(Enum):
    """File types for Helix bundle, setlist, and preset files.
    
    Attributes:
        BUNDLE (str): The bundle file type.
        SETLIST (str): The setlist file type.
        PRESET (str): The preset file type.

    Examples:
    ``` py
    file_type = FileType.BUNDLE
    ```
    """

    BUNDLE = 'hlb'
    SETLIST = 'hls'
    PRESET = 'hlx'

    @classmethod
    def get_type(cls, file_path: str) -> 'FileType':
        """Returns the file type based on the file extension.
        
        Args:
            file_path (str): The path to the file.
        
        Returns:
            FileType: The file type.

        Examples:
        ``` py
        FileType.get_type(file_path)
        ```
        """
        file_extension = file_path.split('.')[-1].lower()
        for member in cls:
            if file_extension == member.value:
                return member
        return None
    
    @classmethod
    def get_extension_by_name(cls, name: str) -> str:
        """Returns the file extension based on the file type name.
        
        Args:
            name (str): The name of the file type.
        
        Returns:
            str: The file extension.

        Examples:
        ``` py
        name = 'bundle'
        extension = FileType.get_extension_by_name(name)
        ```
        """
        name = name.upper()
        if name in cls.__members__:
            return cls[name].value
        raise ValueError(f"{name} is not a valid FileType name")
    
    @classmethod
    def get_member_by_name(cls, name: str) -> 'FileType':
        """Returns the file type based on the file type name.
        
        Args:
            name (str): The name of the file type.
        
        Returns:
            FileType: The file type.

        Examples:
        ``` py
        name = 'bundle'
        member = FileType.get_member_by_name(name)
        ```
        """
        name = name.upper()
        if name in cls.__members__:
            return cls[name]
        raise ValueError(f"{name} is not a valid FileType name")
    
    @classmethod
    def exists_by_name(cls, name: str) -> bool:
        """Checks if a file type exists based on the file type name.

        Args:
            name (str): The name of the file type.
        
        Returns:
            bool: Whether the file type exists or not.

        Examples:
        ``` py
        name = 'bundle'
        exists = FileType.exists_by_name(name)
        ```
        """
        name = name.upper()
        return name in cls.__members__

class TemplatePath(Enum):
    """Template paths for Helix bundle, setlist, and preset files."""
    BUNDLE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates', 'bundle.hlb'))
    SETLIST = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates', 'setlist.hls'))
    PRESET = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates', 'preset.hlx'))

    @classmethod
    def get_by_file_type(cls, file_type: FileType) -> str:
        """Returns the template path based on the file type.
        
        Args:
            file_type (FileType): The file type.
        
        Returns:
            TemplatePath: The template path.

        Examples:
        ``` py
        file_type = FileType.BUNDLE
        TemplatePath.get_by_file_type(file_type)
        ```
        """
        if file_type:
            if file_type == FileType.BUNDLE:
                return TemplatePath.BUNDLE.value
            elif file_type == FileType.SETLIST:
                return TemplatePath.SETLIST.value
            elif file_type == FileType.PRESET:
                return TemplatePath.PRESET.value
        return None

    @classmethod
    def get_by_file_path(cls, file_path: str) -> str:
        """Returns the template path based on the file type.
        
        Args:
            file_path (str): The path to the file.
        
        Returns:
            TemplatePath: The template path.

        Examples:
        ``` py
        file_path = '/path/to/file.hlx'
        TemplatePath.get_template_path(file_path)
        ```
        """
        file_type = FileType.get_type(file_path)
        return TemplatePath.get_by_file_type(file_type)
    
    @classmethod
    def get_by_file_type_name(cls, type_name: str) -> str:
        """Returns the template path based on the file type name.
        
        Args:
            type_name (str): The name of the file type.
        
        Returns:
            TemplatePath: The template path.

        Examples:
        ``` py
        type_name = 'bundle'
        TemplatePath.get_by_file_type_name(type_name)
        ```
        """
        file_type = FileType.get_member_by_name(type_name)
        return TemplatePath.get_by_file_type(file_type=file_type)

    
class Files:
    """Performs operations on Helix bundle, setlist, and preset files."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def _get_unique_filename(file_name):
        base, ext = os.path.splitext(file_name)
        counter = 1
        new_file_name = file_name

        while os.path.exists(new_file_name):
            new_file_name = f"{base} ({counter}){ext}"
            counter += 1

        return new_file_name

    @staticmethod
    def _check_existing_file(file_path: str) -> None:
        """
        Validates if a file is readable and writable.

        Args:
            file_path (str): The path to the file.

        Raises:
            Exception: If the file is not readable and writable.

        Examples:
        ``` py
        Files._check_existing_file(file_path)
        ```

        Returns:
            None
        """
        if not file_path:
            raise Exception('File path not provided.')
        
        if not os.path.exists(file_path):
            raise Exception('File does not exist.')

        if not os.path.isfile(file_path):
            raise Exception('File is not a file.')

        if not os.access(file_path, os.R_OK):
            raise Exception('File is not readable.')
        
        Files._check_nonexisting_file(file_path)
        
    @staticmethod
    def _check_nonexisting_file(file_path: str) -> None:
        """
        Validates if a file is writable.

        Args:
            file_path (str): The path to the file.

        Raises:
            Exception: If the file is not writable.

        Examples:
        ``` py
        Files._check_nonexisting_file(file_path)
        ```

        Returns:
            None    
        """
                
        if not FileType.get_type(file_path):
            raise Exception('File extension is not valid for bundle, setlist, or preset.')
        
        directory = os.path.dirname(file_path)
        if not os.path.isdir(directory):
            raise Exception("Directory does not exist:", directory)

        if not os.access(directory, os.W_OK):
            raise Exception("Directory is not writable:", directory)
            
    @staticmethod
    def _decode_data(data: dict) -> bytes:
        """
        Base 64 decodes data.
        
        Args:
            data (dict): The data to decode.
        
        Returns:
            bytes: The decoded data.

        Examples:
        ``` py
        Files._decode_data(data)
        ```

        Returns:
            bytes
        """
        return base64.b64decode(data)

    @staticmethod
    def _encode_data(data):
        """
        Base 64 encodes data.
        
        Args:
            data (bytes): The data to encode.
        
        Returns:
            str: The encoded data.

        Examples:
        ``` py
        Files._encode_data(data)
        ```

        Returns:
            str
        """
        return base64.b64encode(data).decode('utf-8')

    @staticmethod
    def _decompress_data(compressed_data):
        """
        Zlib decompresses data.
        
        Args:
            compressed_data (bytes): The data to decompress.
        
        Returns:
            bytes: The decompressed data.

        Examples:
        ``` py
        Files._decompress_data(compressed_data)
        ```

        Returns:
            bytes
        """
        return zlib.decompress(compressed_data)

    @staticmethod
    def _compress_data(data:dict):
        """
        Zlib compresses data.
        
        Args:
            data (dict): The data to compress.
        
        Returns:
            bytes: The compressed data.

        Examples:
        ``` py
        Files._compress_data(data)
        ```

        Returns:
            bytes
        """
        return zlib.compress(data)

    @staticmethod
    def _import_file(file_path):
        """
        Imports a bundle, setlist, or preset file.
        
        All contents of a preset file is returned as "data".
        All contents of bundle and setlist "encoded_data" key is decoded, decompressed, and returned as "data".
        All other keys from bundle and setlist are returned as "metadata".

        Returns:
            tuple: (data, metadata)

        Examples:
        ``` py
        Files._import_file(file_path)
        ```
        """
        Files._check_existing_file(file_path)

        with open(file_path, 'r') as file:
            file_data = json.load(file)

            if FileType.get_type(file_path) == FileType.PRESET:
                return file_data, {}
            
            # decode
            encoded_data = file_data.pop('encoded_data')
            decoded_data = Files._decode_data(encoded_data)

            # decompress
            decompressed_data = Files._decompress_data(decoded_data)
            decompressed_data = decompressed_data.strip().decode('utf-8')
            decompressed_data = json.loads(decompressed_data)

            return decompressed_data, file_data

    @staticmethod
    def _export_file(file_path, data, metadata):
        """
        Exports a bundle, setlist, or preset file.
        
        Args:
            file_path (str): The path to the file to export.
            data (dict): The data to export.
            metadata (dict): The metadata to export.

        Examples:    
        ```
        Files._export_file(file_path, data, metadata)
        ```
        """
        # error if file path is bad
        Files._check_nonexisting_file(file_path)        

        if FileType.get_type(file_path) == FileType.PRESET:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=1)
            return

        # error if template file path is bad
        template_file_path = TemplatePath.get_by_file_path(file_path)
        Files._check_existing_file(template_file_path)

        # Create a copy of data to avoid modifying the original
        data_copy = data.copy()        

        # save to later set in hlb/hls header
        if FileType.get_type(file_path) == FileType.SETLIST:
            name = data_copy["meta"]["name"]
        else:
            name = metadata["meta"]["name"]

        decoded_data = data_copy
        data_copy = json.dumps(decoded_data, separators=(',', ':'))
        data_copy = data_copy.encode('utf-8')

        compressed_data = Files._compress_data(data_copy)
        encoded_data = Files._encode_data(compressed_data)
        crc32_value = binascii.crc32(data_copy)

        if not metadata:
            with open(template_file_path, 'r') as file:
                metadata = json.load(file)
                metadata.pop('encoded_data')

        metadata['meta']['name'] = name
        metadata["meta"]["modifieddate"] = int(time.time())

        metadata["encoded_data"] = encoded_data

        metadata["compression"]["decompressed_size"] = len(data_copy)
        metadata["compression"]["crc32"] = crc32_value
 
        with open(file_path, 'w') as file:
            json.dump(metadata, file, indent=1)