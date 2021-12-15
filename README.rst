===================
Stratocumulus
===================

|PyPI| |Python| |License|

.. |PyPI| image:: https://img.shields.io/pypi/v/stratocumulus.svg
   :target: https://pypi.org/project/stratocumulus

.. |Python| image:: https://img.shields.io/pypi/pyversions/stratocumulus.svg
   :target: https://pypi.org/project/stratocumulus

.. |License| image:: https://img.shields.io/github/license/lilab-bcb/stratocumulus
   :target: https://github.com/lilab-bcb/stratocumulus/blob/master/LICENSE

Stratocumulus is the backend component of `Cumulus <https://github.com/klarman-cell-observatory/cumulus>`_, which aims to providing a unified backend interface for different cloud environments.

Installation
+++++++++++++++

Stratocumulus does not include any Cloud SDK. You need to install the corresponding SDK separately, depending on which Cloud platform you use:

* Google Cloud: Install `Google Cloud SDK <https://cloud.google.com/sdk/docs/install>`_.
* Amazon AWS: Install `AWS CLI <https://aws.amazon.com/cli/>`_.
* Local machine: Works for Linux and macOS. Please make sure **rsync** is installed, as some commands will use it.

After that, install Stratocumulus in your Python environment by command::

    pip install stratocumulus

Usage
++++++

Stratocumulus has 4 commands:

* ``cp``: Copy file(s)/folder(s).
* ``sync``: Synchronize two folders, usually used for copying one folder.
* ``rm``: Remove file(s)/folder(s).
* ``exist``: Check if a (remote) file/folder exists.

These commands have options specific to backend. For now, Stratocumulus supports the following backends:

* ``aws``: Amazon AWS.
* ``gcp``: Google Cloud.
* ``local``: Local machine. In specific, macOS or Linux.

``cp``
^^^^^^^^^^

This command copies file(s) or folder(s). See examples below::

   # AWS upload
   strato cp --backend aws file1 folder2 s3://my-bucket/target_folder/
   # AWS download
   strato cp --backend aws s3://my-bucket/source_folder/*.zip /target_folder/

   # GCP upload
   strato cp --backend gcp -m -r --ionice file1 folder2 gs://my-bucket/target_folder/
   # GCP download
   mkdir /target_folder
   strato cp --backend gcp -m gs://my-bucket/source_folder/*.zip /target_folder/

   # Local Machine
   strato cp --backend local -r file1 folder2 /target_folder/

Notice that:

* For AWS backend, you must explicitly attach a trailing slash for source folder.
* For Google Cloud download, you'll have to explicitly create the target folder, and then run ``strato cp`` command.
* Wildcards are acceptable.
* ``-r`` option is not needed for AWS, and copying folders is always recursive.
* ``-m`` and ``--ionice`` options only work for Google Cloud.

For details on the options, try command ``strato cp -h``.

``sync``
^^^^^^^^^^^

This command synchronizes two folders. Notice that this synchronization will delete content in the target folder not existing in the source folder.

See examples below::

   # AWS
   strato sync --backend aws source_folder s3://my-bucket/target_folder
   # GCP
   strato sync --backend gcp -m --ionice source_folder gs://my-bucket/target_folder
   # Local Machine
   strato sync --backend local source_folder target_folder

Notice that:

* ``-m`` and ``--ionice`` options only work for Google Cloud.

For details on the options, try command ``strato sync -h``.

``rm``
^^^^^^^^^

This command deletes file(s) or folder(s). See examples below::

   # AWS
   strato rm --backend aws s3://my-bucket/file1 s3://my-bucket/folder2/
   # GCP
   strato rm --backend gcp -m gs://my-bucket/file1 gs://my-bucket/folder2 gs://my-bucket/folder3/*.zip
   # Local Machine
   strato rm --backend local file1 folder2

Notice that:

* ``-m`` option only works for Google Cloud.
* For AWS backend, wildcards are not yet accepted.

For details on the options, try command ``strato rm -h``.

``exists``
^^^^^^^^^^^^^

This command checks if a (remote) file or folder exists. If it exists, the command terminates without any output.
Otherwise, the command will break with Python ``subprocess.CalledProcessError`` exception.

See examples below::

   # AWS
   strato exists --backend aws s3://my-bucket/file1
   # GCP
   strato exists --backend gcp gs://my-bucket/folder2/
   # Local Machine
   strato exists --backend local folder2/

Notice that this command works for both file and folder, regardless of backend.

For details on the options, try command ``strato exists -h``.

``help``
^^^^^^^^^^

Type ``strato -h`` or ``strato --help`` to check available Stratocumulus commands.

Check version
^^^^^^^^^^^^^^^

Type ``strato -v`` or ``strato --version`` to check the version of Stratocumulus currently installed on your machine.
