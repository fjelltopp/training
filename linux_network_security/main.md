# Permissions and ownership
## Users and groups
Users and groups are used on Linux for access control to the system's files directories and periferials.

There's a one special user **root** - the administrator user:
* it has no access restriction and so should be used with caution
* to remind about this its command prompt is `#` instead of usual `$`
    ```bash
    # the administrator
    root@ubuntu:/# 

    # normal user
    tomek@ubuntu:/$ 
    ```
* to minimize security risk there exists a command `sudo` = "do as root"
    ```bash
    tomek@ubuntu:/$ whoami
    # tomek
    tomek@ubuntu:/$ sudo whoami
    # root
    ```


#### Users
```bash
useradd -m -g initial_group -G additional_groups username
# e.g. 
useradd -m tomek
```
* `-m` creates the user home directory as `/home/username`
* `-g` defines the group name 
* `-G` introduces a list of supplementary groups which the user is also a member of

You can log in as the new user with `su` command:
```bash
root@ubuntu: /# su tomek
tomek@ubuntu:/$
```
To log out press <kbd>Ctrl</kbd>+<kbd>d</kbd>.

To **change password** use:
```bash
tomek@ubuntu:/$ passwd
# Changing password for tomek.
# (current) UNIX password: 
# Enter new UNIX password: 
# Retype new UNIX password: 
# passwd: password updated successfully

root@ubuntu:/# passwd tomek
# Enter new UNIX password: 
# Retype new UNIX password: 
# passwd: password updated successfully
```

More modifications can be made with `usermod` which is greatly described in its man page:
```bash
# to modify user home directory, username, and more:
man usermod
```

#### Groups

Each user has a default group with the same name. E.g.
```bash
groups tomek
# tomek : tomek
```
Adding a new group is very easy:
```bash
groupadd WHO
```
And later assigning an existing user to the group:
```bash
gpasswd -a tomek WHO
```
With the result:
```bash
groups tomek
# tomek : tomek WHO
```
To remove a user from the group:
```bash
gpasswd -??? user group # use man gpasswd
```
To change group name:
```bash
groupmod -n new_group old_group
```
To remove the group:
```bash
groupdel group
```

#### Excercise:
Bla bla bla

## What are files?
In Linux everything is a file.
* a regular text file
    ```bash
    cat dog.txt
    # Bark!
    ```
* various media
    ```bash
    ls -l /media/
    # drwxr-x---+ 2 root root 4096 Sep  3 00:57 tomek

    $ ls -l /media/tomek 
    # drwxrwxrwx 1 tomek tomek 12288 Jun  6 08:47 TOURO
    ```
* and even I/O devices
    ```bash
    # simple audio playback & recording
    cat /dev/audio > my_file
    cat my_file > /dev/audio
    ```

### Permissions
Simple listing of directory content looks like that:
```bash
ls -la
# drwxrwxr-x  2 tomek tomek  4096 Sep 18 13:40 images
# -rw-rw-r--  1 tomek tomek   631 Sep 18 13:39 main.md
```
First column represents permission to the file.
```bash
drwxrwxr-x

# directory? | owner | group | rest of the world
# d or -     | read write execute with r w x present in order
```

#### Modifying file permission and ownership
```bash
chmod a,u,g+/-x/w/r
chmod 755

chown user:group
```

# Links and readings
* https://wiki.archlinux.org/index.php/users_and_groups
* 
