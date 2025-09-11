import zipfile
import time
import string
import itertools
import os
import io
import multiprocessing
from functools import partial

def generate_password_batch(charset, length, batch_size, start_idx):
    """Generate a batch of passwords starting from start_idx."""
    passwords = []
    chars = list(charset)
    iterator = itertools.product(chars, repeat=length)
    for i, combo in enumerate(iterator):
        if i < start_idx:
            continue
        if len(passwords) >= batch_size:
            break
        passwords.append(''.join(combo))
    return passwords, i + 1

def try_password(password, zip_data):
    """Test a single password on the in-memory zip file."""
    try:
        with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zip_file:
            zip_file.setpassword(password.encode('utf-8'))
            if zip_file.testzip() is None:
                return password
            return None
    except RuntimeError:
        return None
    except Exception as e:
        if 'Error -3' in str(e):
            return 'zlib_error'
        print(f'Unexpected error in try_password for {password}: {e}', flush=True)
        return None

def validate_zip(zip_path):
    """Validate zip file before processing."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            zip_file.testzip()
        print(f'Warning: {zip_path} is not password-protected.', flush=True)
        return False
    except zipfile.BadZipFile:
        print(f'Error: {zip_path} is not a valid zip file.', flush=True)
        return False
    except RuntimeError as e:
        if 'encrypted' in str(e).lower():
            return True
        print(f'Error validating zip file: {e}', flush=True)
        return False
    except Exception as e:
        print(f'Unexpected error validating zip file: {e}', flush=True)
        return False

def unlock_zip(zip_path='week8/emergency_storage_key.zip', output_file='password.txt',
               length=6, charset=string.ascii_lowercase + string.digits, batch_size=100000000):
    """Unlock zip file using optimized multiprocessing and in-memory batches."""
    start_time = time.time()
    attempt_count = 0
    zlib_error_count = 0
    
    print('Starting password cracking process...', flush=True)
    print(f'Start time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))}', flush=True)
    print(f'Using charset: {charset}, Password length: {length}', flush=True)
    print(f'Batch size: {batch_size}, Using {multiprocessing.cpu_count()} processes.', flush=True)
    
    # Validate zip file
    if not validate_zip(zip_path):
        return None
    
    # Load zip file into memory
    try:
        with open(zip_path, 'rb') as f:
            zip_data = f.read()
    except FileNotFoundError:
        print(f'Error: Zip file {zip_path} not found.', flush=True)
        return None
    except Exception as e:
        print(f'Error loading zip file: {e}', flush=True)
        return None
    
    # Initialize multiprocessing pool
    num_processes = min(multiprocessing.cpu_count(), 4)  # Limit to 4 cores
    pool = multiprocessing.Pool(processes=num_processes)
    start_idx = 0
    
    # Optimize chunksize for 4 cores
    chunksize = max(5000, batch_size // num_processes // 2)
    print(f'Using chunksize: {chunksize}', flush=True)
    
    while True:
        # Generate batch of passwords
        print(f'Generating batch starting at index {start_idx}...', flush=True)
        passwords, next_idx = generate_password_batch(charset, length, batch_size, start_idx)
        if not passwords:
            break
        
        attempt_count += len(passwords)
        # Test passwords in parallel
        try_password_func = partial(try_password, zip_data=zip_data)
        results = []
        batch_progress = 0
        for i, result in enumerate(pool.imap_unordered(try_password_func, passwords, chunksize=chunksize)):
            results.append(result)
            batch_progress += 1
            if result == 'zlib_error':
                zlib_error_count += 1
            if batch_progress % 5000000 == 0:
                progress_percent = (batch_progress / len(passwords)) * 100
                elapsed = time.time() - start_time
                print(f'Batch progress: {progress_percent:.1f}%, Attempts: {attempt_count - len(passwords) + batch_progress}, '
                      f'Elapsed time: {elapsed:.2f} seconds, Zlib errors: {zlib_error_count}', flush=True)
        
        # Check if all attempts failed with zlib errors
        if zlib_error_count >= len(passwords):
            print(f'\nError: All {len(passwords)} attempts in this batch failed with zlib errors.', flush=True)
            print('Likely cause: The zip file is corrupted or not compatible with Python zipfile.', flush=True)
            print('Please verify the zip file or replace it with a valid password-protected zip file.', flush=True)
            pool.close()
            pool.join()
            return None
        
        # Check for successful password
        for password in results:
            if isinstance(password, str) and password != 'zlib_error':
                # Verify with extraction
                try:
                    with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zip_file:
                        zip_file.setpassword(password.encode('utf-8'))
                        zip_file.extractall(path='temp_extract')
                        if os.path.exists('temp_extract'):
                            for root, _, files in os.walk('temp_extract'):
                                for file in files:
                                    os.remove(os.path.join(root, file))
                            os.rmdir('temp_extract')
                    elapsed = time.time() - start_time
                    print(f'\nSuccess! Password found: {password}', flush=True)
                    print(f'Total attempts: {attempt_count}', flush=True)
                    print(f'Total time: {elapsed:.2f} seconds', flush=True)
                    
                    # Save password to file
                    try:
                        with open(output_file, 'w') as f:
                            f.write(password)
                        print(f'Password saved to {output_file}', flush=True)
                    except IOError as e:
                        print(f'Error saving password to file: {e}', flush=True)
                    
                    pool.close()
                    pool.join()
                    return password
                except Exception as e:
                    print(f'Extraction failed for {password}: {e}', flush=True)
                    continue
        
        start_idx = next_idx
        elapsed = time.time() - start_time
        print(f'Batch completed. Total attempts: {attempt_count}, Elapsed time: {elapsed:.2f} seconds', flush=True)
    
    pool.close()
    pool.join()
    elapsed = time.time() - start_time
    print(f'\nFailed to find password after {attempt_count} attempts.', flush=True)
    print(f'Total time: {elapsed:.2f} seconds', flush=True)
    return None

if __name__ == '__main__':
        unlock_zip()
        
        
        # 해결방법
        # MEMORY에 올려서 작업할 것. 
        # 파일 압축 해제 하지 말 것. EXTRACT 제거. 
        # FOR문으로 돌려서 하면 더 빠름. 
        # POOL()을 사용해서 최대 CPU 코어를 사용해 멀티프로세스 동자 구현.
        # 6자리 중 첫 번째 자리로 멀티 스레드를 각각 동작시킴. 나머지 5자리에 대해 FOR문 돌려서 찾기
        
        
        
        