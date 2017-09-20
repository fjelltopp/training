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


### Users
#### Create new user

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

#### Change user's password
When typing passwords in linux console you won't see any characters (`*` or `•`) for security reasons.

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

### Groups

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

## With the result:
groups tomek
# tomek : tomek WHO
```

To remove a user from the group:

```bash
gpasswd -??? user group     # Exercise: find ??? using man gpasswd
```

Or to change group name:

```bash
groupmod -n UN WHO          # new_name old_name
```

And to remove the group:
```bash
groupdel WHO                # group_name
```

### Excercise:
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
  
You can access **any service and resource** in the system by accessing **a file in the filesystem**.

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
Various permission representations:

```bash
## if instead of letters we use 0 and 1 we get:
  user  | group | all
  rwx   |  r-x  | ---
  111   |  101  | 000       # binary
   7    |   5   |  0        # decimal
```

##### File permissions
To change permission use `chmod` command:

```bash
chmod 755 dog.txt
```

Or using aliases

```bash
chmod a+r dog.txt       # gives read permission for all users
chmod a,u,g+/-x/w/r
```

* `+` to add permissions
* `-` to remove permissions
* `=` to set permissions
* `u` is user
* `g` is group
* `a` is all

More examples:
* `chmod ga-rw dog.txt` removes read & write permissions for group and all
* `chmod g=rw` sets group permissions to `rw-`

##### Ownership
Change file ownership with `chown`:

```bash
chown user:group
```

### Exercise
Lorem ipsum

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

# Network
## Basic network commands
### ifconfig

```bash
tomek@ubuntu:~$ ifconfig
# eth0      Link encap:Ethernet  HWaddr 02:76:22:67:e9:bc  
#           inet addr:10.0.1.27  Bcast:10.0.1.255  Mask:255.255.255.0
#           inet6 addr: fe80::76:22ff:fe67:e9bc/64 Scope:Link
#           UP BROADCAST RUNNING MULTICAST  MTU:9001  Metric:1
#           RX packets:890 errors:0 dropped:0 overruns:0 frame:0
#           TX packets:839 errors:0 dropped:0 overruns:0 carrier:0
#           collisions:0 txqueuelen:1000 
#           RX bytes:100925 (100.9 KB)  TX bytes:115527 (115.5 KB)
# 
# lo        Link encap:Local Loopback  
#           inet addr:127.0.0.1  Mask:255.0.0.0
#           inet6 addr: ::1/128 Scope:Host
#           UP LOOPBACK RUNNING  MTU:65536  Metric:1
#           RX packets:184 errors:0 dropped:0 overruns:0 frame:0
#           TX packets:184 errors:0 dropped:0 overruns:0 carrier:0
#           collisions:0 txqueuelen:1 
#           RX bytes:16126 (16.1 KB)  TX bytes:16126 (16.1 KB)

#################
itomek@ubuntu:~$ fconfig eth0     # for more specific output

```

### ping
PING (Packet INternet Groper) command is the best way to test connectivity between two nodes.

```bash
 ping google.com
 #PING google.com (172.217.18.78) 56(84) bytes of data.
 #64 bytes from bud02s26-in-f14.1e100.net (172.217.18.78): icmp_seq=1 ttl=52 time=77.9 ms
 #64 bytes from bud02s26-in-f14.1e100.net (172.217.18.78): icmp_seq=2 ttl=52 time=76.0 ms
 #64 bytes from bud02s26-in-f14.1e100.net (172.217.18.78): icmp_seq=3 ttl=52 time=84.4 ms
 #64 bytes from bud02s26-in-f14.1e100.net (172.217.18.78): icmp_seq=4 ttl=52 time=92.2 ms
 #^C
 #--- google.com ping statistics ---
 #4 packets transmitted, 4 received, 0% packet loss, time 3005ms
 #rtt min/avg/max/mdev = 76.017/82.665/92.240/6.348 ms
```

Kill it with <kbd>Ctrl</kbd> + <kbd>C</kbd>


### traceroute
Prints the route of packages on the way to host.

```bash
traceroute 4.2.2.2
# traceroute to 4.2.2.2 (4.2.2.2), 30 hops max, 60 byte packets
# 1  192.168.50.1 (192.168.50.1)  0.217 ms  0.624 ms  0.133 ms
# 2  227.18.106.27.mysipl.com (27.106.18.227)  2.343 ms  1.910 ms  1.799 ms
# 3  221-231-119-111.mysipl.com (111.119.231.221)  4.334 ms  4.001 ms  5.619 ms
# 4  10.0.0.5 (10.0.0.5)  5.386 ms  6.490 ms  6.224 ms
# 5  gi0-0-0.dgw1.bom2.pacific.net.in (203.123.129.25)  7.798 ms  7.614 ms  7.378 ms
# 6  115.113.165.49.static-mumbai.vsnl.net.in (115.113.165.49)  10.852 ms  5.389 ms  4.322 ms
# 7  ix-0-100.tcore1.MLV-Mumbai.as6453.net (180.87.38.5)  5.836 ms  5.590 ms  5.503 ms
# 8  if-9-5.tcore1.WYN-Marseille.as6453.net (80.231.217.17)  216.909 ms  198.864 ms  201.737 ms
# 9  if-2-2.tcore2.WYN-Marseille.as6453.net (80.231.217.2)  203.305 ms  203.141 ms  202.888 ms
# 10  if-5-2.tcore1.WV6-Madrid.as6453.net (80.231.200.6)  200.552 ms  202.463 ms  202.222 ms
# 11  if-8-2.tcore2.SV8-Highbridge.as6453.net (80.231.91.26)  205.446 ms  215.885 ms  202.867 ms
# 12  if-2-2.tcore1.SV8-Highbridge.as6453.net (80.231.139.2)  202.675 ms  201.540 ms  203.972 ms
# 13  if-6-2.tcore1.NJY-Newark.as6453.net (80.231.138.18)  203.732 ms  203.496 ms  202.951 ms
# 14  if-2-2.tcore2.NJY-Newark.as6453.net (66.198.70.2)  203.858 ms  203.373 ms  203.208 ms
# 15  66.198.111.26 (66.198.111.26)  201.093 ms 63.243.128.25 (63.243.128.25)  206.597 ms 66.198.111.26 (66.198.111.26)  204.178 ms
# 16  ae9.edge1.NewYork.Level3.net (4.68.62.185)  205.960 ms  205.740 ms  205.487 ms
# 17  vlan51.ebr1.NewYork2.Level3.net (4.69.138.222)  203.867 ms vlan52.ebr2.NewYork2.Level3.net (4.69.138.254)  202.850 ms vlan51.ebr1.NewYork2.Level3.net (4.69.138.222)  202.351 ms
# 18  ae-6-6.ebr2.NewYork1.Level3.net (4.69.141.21)  201.771 ms  201.185 ms  201.120 ms
# 19  ae-81-81.csw3.NewYork1.Level3.net (4.69.134.74)  202.407 ms  201.479 ms ae-92-92.csw4.NewYork1.Level3.net (4.69.148.46)  208.145 ms
# 20  ae-2-70.edge2.NewYork1.Level3.net (4.69.155.80)  200.572 ms ae-4-90.edge2.NewYork1.Level3.net (4.69.155.208)  200.402 ms ae-1-60.edge2.NewYork1.Level3.net (4.69.155.16)  203.573 ms
# 21  b.resolvers.Level3.net (4.2.2.2)  199.725 ms  199.190 ms  202.488 ms
```

### netstat
Swiss army knife for networking.

```bash
netstat -a | grep ssh
# tcp        0      0 *:ssh                   *:*                     LISTEN     
# tcp        0     36 ip-10-0-1-27.eu-wes:ssh user-31-175-161-1:47310 ESTABLISHED
# tcp        0      0 ip-10-0-1-27.eu-wes:ssh user-31-175-161-1:43680 ESTABLISHED
# tcp        0      0 ip-10-0-1-27.eu-wes:ssh user-31-175-161-1:53704 ESTABLISHED
# tcp6       0      0 [::]:ssh                [::]:*                  LISTEN 
```

For more please see `man netstat` or links at the end.

# Links and readings

* https://wiki.archlinux.org/index.php/users_and_groups
* https://help.ubuntu.com/community/SSH/OpenSSH/Keys
* https://www.digitalocean.com/community/tutorials/how-to-protect-ssh-with-fail2ban-on-ubuntu-14-04
* https://www.tecmint.com/20-netstat-commands-for-linux-network-management/

