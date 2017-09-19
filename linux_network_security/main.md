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

### Exercise
Lorem ipsum

#Network
## Basic network commands
## Firewalls
fail2ban
# 

# SSH - secure shell
## Remote login and command execution
```bash
ssh remoteuser@hostname
# e.g. ssh tomek@meerkat.org
```
#### SSH and pipes
```bash
tar czf - /home/user/files | ssh user@remote_host tar -xvzf -C /remote/path/
```
Example:
```bash
ssh tomek@localhost
# The authenticity of host 'localhost (::1)' can't be established.
# ECDSA key fingerprint is SHA256:tfK0Ja8BrcSgKYh1mE+uzShwT6stj4Jim0qWdXiNqjE.
# Are you sure you want to continue connecting (yes/no)? yes
# Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
tomek@localhost's password: 
# Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.10.0-33-generic x86_64)
# 
#  * Documentation:  https://help.ubuntu.com
#  * Management:     https://landscape.canonical.com
#  * Support:        https://ubuntu.com/advantage
# 
# The programs included with the Ubuntu system are free software;
# the exact distribution terms for each program are described in the
# individual files in /usr/share/doc/*/copyright.
# 
# Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
# applicable law.
# 
$ 

```
But passwords are not that convenient. The solution is:
## RSA keys
#### Making your life easier
```bash
ls -l ~/.ssh
-rw------- 1 tomek tomek 3326 Jun  4 22:03 id_rsa      # private part of rsa key
-rw-r--r-- 1 tomek tomek  748 Jun  4 22:03 id_rsa.pub  # public part of rsa key
-rw------- 1 tomek tomek 1140 Sep 19 14:12 authorized_keys
-rw-rw-r-- 1 tomek tomek  119 Jul 27 15:17 config      # custom configuration
-rw-r--r-- 1 tomek tomek 4642 Aug 30 15:46 known_hosts # list of trusted hosts
```
#### rsa key
Instead of using a password to authenticate during ssh session you may use RSA key pair.
```bash
mkdir ~/.ssh        # create the directory to store ssh user configuration
chmod 700 ~/.ssh    # only owner can access the directory
ssh-keygen -t rsa   # create the rsa key pair

# Generating public/private rsa key pair.
# Enter file in which to save the key (/home/tomek/.ssh/id_rsa): 
# Enter passphrase (empty for no passphrase): 
# Enter same passphrase again: 
# Your identification has been saved in /home/tomek/.ssh/id_rsa.
# Your public key has been saved in /home/tomek/.ssh/id_rsa.pub.
# The key fingerprint is:
# SHA256:jyGCGzsbIFwFSKg7tj9gOC1o4o3U1TNukL7omIch5VU tomek@ca2ae63ebde1
# The key's randomart image is:
# +---[RSA 2048]----+
# |o.....           |
# |..  . E          |
# |.  . .o          |
# |o o..+ +         |
# |=*+.+ + S        |
# |@Oo= o + +       |
# |O+% . o . .      |
# | =oO .           |
# | o=o.            |
# +----[SHA256]-----+
# 
```
Now you should see two new files `id_rsa` and `id_rsa.pub` in your `~/.ssh` directory.
* **id_rsa.pub** the public part of the key. To be shared with others and added to `.ssh/authorized_keys` file on remote machines.

  This can be done by manually appending content of `id_rsa.pub` to `authorized_keys` or with help of the following command:
  ```bash
    ssh-copy-id tomek@localhost   # <username>@<host>
    /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/tomek/.ssh/id_rsa.pub"
  # The authenticity of host 'localhost (::1)' can't be established.
  # ECDSA key fingerprint is SHA256:tfK0Ja8BrcSgKYh1mE+uzShwT6stj4Jim0qWdXiNqjE.
  # Are you sure you want to continue connecting (yes/no)? yes
  # /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
  # /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
  # tomek@localhost's password: 
  # 
  # Number of key(s) added: 1
  # 
  # Now try logging into the machine, with:   "ssh 'tomek@localhost'"
  # and check to make sure that only the key(s) you wanted were added.
  # 
  # tomek@ca2ae63ebde1:/$ cat ~/.ssh/authorized_keys 
  # ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDGflus6n/66gSy3efx/j7OcB6L+kRzfXSyA74Gi9zE1WuNLkrAyvCeSmSisQVygIanWZNbLRuG0zB/eG6T
  # hbt2pjXQ3deQv5ifmQSR6D5aPKd3vwd1nxKgb4oXTqnAkWOlNYzQi80hwNfjxl46qBMuM1sApHlW8ckSi8m51MeM+TIp+sNJ5VWThEICZopzNM+zBFtoSy04
  # 8kod6wTzmBCvXFJVb9+gOwcZLrYZFYxPZcQWcqGCerfJpT9N2rZrpsizYiyp1A1dvR/RnRh7x5dflGbz0CVCLznwm1KOsrdPMU0OQ0RkHHZs3kEhq7ZAy2mt
  # UE7RxtZAW6bqnpCxAhT9 tomek@ubuntu
  ```
  Now you can log passwordless with just using:
  ```bash
    ssh tomek@localhost
  ```
* **id_rsa** the private part. Do not share it with anyone! Keep it secret.
  ```bash
    ssh -i ~/.ssh/second_id_rsa tomek@ubuntu  # using custom RSA key as identity
  ```
#### config
```bash
cat ~/.ssh/config
## the description of the server
# Host meerkat
#    HostName 127.0.0.1 # or meerkat.org
#    Port 22000 # optional, 22000 is default
#    User ubuntu # user to be used by ssh
```
#### known_hosts
List of trusted hosts with their secure fingerprint. Important for preventing *man in the middle* attacks.



# Links and readings
* https://wiki.archlinux.org/index.php/users_and_groups
* 
