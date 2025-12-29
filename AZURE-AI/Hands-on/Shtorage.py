import os
import asyncio
from typing import List, Optional, Dict
from azure.storage.blob.aio import BlobServiceClient
from azure.core.exceptions import AzureError, ResourceExistsError, ResourceNotFoundError


class AzureStorageManager:
    """
    A professional, fully asynchronous Azure Blob Storage Manager.
    
    Optimized for high-concurrency applications with comprehensive error handling,
    proper docstrings, and support for file and folder operations.
    
    Attributes:
        connection_string (str): Azure Blob Storage connection string.
    """

    def __init__(self, connection_string: str):

        """
        Initialize the Azure Storage Manager.
        
        Args:
            connection_string (str): Azure Blob Storage connection string.
            
        Raises:
            ValueError: If connection string is empty or None.
        """
        if not connection_string:
            raise ValueError("Azure Connection String is required.")
        self.connection_string = connection_string
        print("  Azure Storage Manager initialized successfully")
    
    async def _get_client(self) -> BlobServiceClient:
        """
        Internal method to get an asynchronous BlobServiceClient.
        
        Returns:
            BlobServiceClient: An instance of the asynchronous BlobServiceClient.
        """
        return BlobServiceClient.from_connection_string(self.connection_string)

    async def create_container(self, container_name: str) -> bool:
        """
        Create a new container in Azure Blob Storage.
        
        Args:
            container_name (str): Name of the container to create.
            
        Returns:
            bool: True if container created or already exists, False on error.
        """
        async with await self._get_client() as service_client:
            try:
                # Attempt to create the container
                await service_client.create_container(container_name)
                print(f"  Container '{container_name}' created successfully.")
                return True
            except ResourceExistsError:
                # Container already exists - this is acceptable
                print(f"⚠ Container '{container_name}' already exists.")
                return True
            except AzureError as e:
                # Azure-specific error occurred
                print(f"   Azure error creating container: {str(e)}")
                return False
            except Exception as e:
                # Unexpected error
                print(f"   Unexpected error creating container: {str(e)}")
                return False

    async def upload_blob(self, container_name: str, blob_name: str, 
                         file_path: str) -> bool:
        """
        Upload a file to Azure Blob Storage as a blob.
        
        Args:
            container_name (str): Name of the target container.
            blob_name (str): Name to assign to the blob in storage.
            file_path (str): Local file path to upload.
            
        Returns:
            bool: True if upload successful, False otherwise.
        """
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Upload file as blob
            async with await self._get_client() as service_client:
                blob_client = service_client.get_blob_client(
                    container=container_name, 
                    blob=blob_name
                )
                # Read file and upload with overwrite enabled
                with open(file_path, "rb") as file_data:
                    await blob_client.upload_blob(file_data, overwrite=True)
                
                print(f"  Blob '{blob_name}' uploaded successfully.")
                return True
                
        except FileNotFoundError as e:
            print(f"   File error: {str(e)}")
            return False
        except AzureError as e:
            print(f"   Azure error uploading blob: {str(e)}")
            return False
        except Exception as e:
            print(f"   Unexpected error uploading blob: {str(e)}")
            return False

    async def upload_folder(self, container_name: str, folder_path: str) -> Dict[str, any]:
        """
        Upload all files from a folder to Azure Blob Storage.
        
        Maintains folder structure in blob names by using relative paths.
        
        Args:
            container_name (str): Name of the target container.
            folder_path (str): Local folder path containing files to upload.
            
        Returns:
            Dict[str, any]: Dictionary containing:
                - status: 'success', 'partial', or 'error'
                - uploaded: List of successfully uploaded blob names
                - errors: List of failed uploads with details
                - count: Number of successfully uploaded files
        """
        uploaded_files = []
        errors = []
        
        try:
            # Validate folder exists
            if not os.path.isdir(folder_path):
                raise NotADirectoryError(f"Not a valid directory: {folder_path}")
            
            async with await self._get_client() as service_client:
                # Walk through all files in folder recursively
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Maintain folder structure in blob names
                        relative_path = os.path.relpath(file_path, folder_path)
                        blob_name = relative_path.replace("\\", "/")
                        
                        try:
                            blob_client = service_client.get_blob_client(
                                container=container_name,
                                blob=blob_name
                            )
                            # Upload file with overwrite enabled
                            with open(file_path, "rb") as file_data:
                                await blob_client.upload_blob(file_data, overwrite=True)
                            
                            print(f"  Uploaded: {blob_name}")
                            uploaded_files.append(blob_name)
                            
                        except Exception as e:
                            # Log individual file upload errors
                            error_msg = str(e)
                            print(f"   Failed to upload {blob_name}: {error_msg}")
                            errors.append({"file": blob_name, "error": error_msg})
            
            # Return summary status
            return {
                "status": "success" if not errors else "partial",
                "uploaded": uploaded_files,
                "errors": errors,
                "count": len(uploaded_files)
            }
            
        except NotADirectoryError as e:
            print(f"   Directory error: {str(e)}")
            return {"status": "error", "details": str(e)}
        except Exception as e:
            print(f"   Unexpected error uploading folder: {str(e)}")
            return {"status": "error", "details": str(e)}

    async def list_blobs(self, container_name: str) -> List[str]:
        """
        List all blob names in a container.
        
        Args:
            container_name (str): Name of the container to list.
            
        Returns:
            List[str]: List of blob names, empty list if container not found.
        """
        async with await self._get_client() as service_client:
            try:
                # Get container client
                container_client = service_client.get_container_client(container_name)
                blob_names = []
                
                # Iterate through async iterator of blobs
                async for blob in container_client.list_blobs():
                    blob_names.append(blob.name)
                
                print(f"  Found {len(blob_names)} blobs in container.")
                return blob_names
                
            except ResourceNotFoundError:
                print(f"   Container '{container_name}' not found.")
                return []
            except AzureError as e:
                print(f"   Azure error listing blobs: {str(e)}")
                return []
            except Exception as e:
                print(f"   Unexpected error listing blobs: {str(e)}")
                return []

    async def download_blob(self, container_name: str, blob_name: str, 
                           download_path: str) -> bool:
        """
        Download a blob from Azure Blob Storage to local file.
        
        Args:
            container_name (str): Name of the container.
            blob_name (str): Name of the blob to download.
            download_path (str): Local file path where blob will be saved.
            
        Returns:
            bool: True if download successful, False otherwise.
        """
        try:
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(download_path), exist_ok=True)
            
            async with await self._get_client() as service_client:
                blob_client = service_client.get_blob_client(
                    container=container_name, 
                    blob=blob_name
                )
                # Download blob and write to file
                download_stream = await blob_client.download_blob()
                
                with open(download_path, "wb") as file:
                    file.write(await download_stream.readall())
                
                print(f"  Blob '{blob_name}' downloaded successfully.")
                return True
                
        except ResourceNotFoundError:
            print(f"   Blob '{blob_name}' not found.")
            return False
        except AzureError as e:
            print(f"   Azure error downloading blob: {str(e)}")
            return False
        except Exception as e:
            print(f"   Unexpected error downloading blob: {str(e)}")
            return False

    async def delete_blob(self, container_name: str, blob_name: str) -> bool:
        """
        Delete a blob from Azure Blob Storage.
        
        Args:
            container_name (str): Name of the container.
            blob_name (str): Name of the blob to delete.
            
        Returns:
            bool: True if deletion successful, False otherwise.
        """
        async with await self._get_client() as service_client:
            try:
                # Get blob client and delete
                blob_client = service_client.get_blob_client(
                    container=container_name, 
                    blob=blob_name
                )
                await blob_client.delete_blob()
                print(f"  Blob '{blob_name}' deleted successfully.")
                return True
                
            except ResourceNotFoundError:
                print(f"   Delete failed: Blob '{blob_name}' not found.")
                return False
            except AzureError as e:
                print(f"   Azure error deleting blob: {str(e)}")
                return False
            except Exception as e:
                print(f"   Unexpected error deleting blob: {str(e)}")
                return False

    async def delete_container(self, container_name: str) -> bool:
        """
        Delete an entire container from Azure Blob Storage.
        
        Args:
            container_name (str): Name of the container to delete.
            
        Returns:
            bool: True if deletion successful, False otherwise.
        """
        async with await self._get_client() as service_client:
            try:
                # Delete container
                await service_client.delete_container(container_name)
                print(f"  Container '{container_name}' deleted successfully.")
                return True
                
            except ResourceNotFoundError:
                print(f"   Container '{container_name}' not found.")
                return False
            except AzureError as e:
                print(f"   Azure error deleting container: {str(e)}")
                return False
            except Exception as e:
                print(f"   Unexpected error deleting container: {str(e)}")
                return False

#--------------------------------------------------------------------------------------------------------------------
import os
from dotenv import load_dotenv

load_dotenv()  

# Example usage and testing
async def main():
    """
    Main function demonstrating AzureStorageManager usage.
    
    Shows examples of all available operations with proper async/await patterns.
    Includes commented examples for each operation type.
    """
    # Get connection string from environment or use default

    connection_string = os.getenv(
        'AZURE_STORAGE_CONNECTION_STRING')
    
    try:
        # Initialize manager
        manager = AzureStorageManager(connection_string)
        
        # Example container name
        container_name = "demo-container"
        
        # # 1. Create container
        # print("\n--- Create Container ---")
        # await manager.create_container(container_name)
        
        # 2. List blobs
        print("\n--- List Blobs ---")
        blobs = await manager.list_blobs(container_name)
        if blobs:
            for i, blob in enumerate(blobs, 1):
                print(f"  {i}. {blob}")
        else:
            print("  No blobs found")
        
        # 3. Upload single file
        print("\n--- Upload File (Uncomment to use) ---")
        # Example: await manager.upload_blob(container_name, "test.txt", "./local/file.txt")
        
        # 4. Upload folder
        print("\n--- Upload Folder (Uncomment to use) ---")
        # result = await manager.upload_folder(container_name, r"C:\Users\raghav.mittal\Downloads\reviews_folder")
        # print(f"  Status: {result['status']}, Uploaded: {result['count']}")
        
        # 5. Download blob
        print("\n--- Download Blob (Uncomment to use) ---")
        # await manager.download_blob(container_name, "reviews_folder/201801.pdf", "./downloads/file.txt")
        
        # 6. Delete blob
        print("\n--- Delete Blob (Uncomment to use) ---")
        # await manager.delete_blob(container_name, "reviews_folder/201801.pdf")
        
        # 7. Delete container
        print("\n--- Delete Container (Uncomment to use) ---")
        # await manager.delete_container(container_name)
        
        print("\n  Demo completed successfully!")
        
    except ValueError as e:
        print(f"   Configuration error: {str(e)}")
    except Exception as e:
        print(f"   Error in main: {str(e)}")



# Entry point for running the script
if __name__ == "__main__":
    asyncio.run(main())


