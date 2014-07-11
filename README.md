Ansible-provision-vms
=========

Ansible-provision-vms is a bunch of playbooks made to provision a host machine and the virtual machines inside it.

At the moment of the write of this document there are two playbooks: **master.yml** and **vms.yml**. The plabook master.yml is used to provision the host server, and the playbook vms.yml is used to create the instances in the host server and provision each virtual machine.

Provision host machine
----------------------

The playbook master.yml use the following roles:

 * [ansible-ssh]
 * [ansible-utils]
 * [ansible-libvirt]
 * [ansible-pxe]
 * [ansible-iptables]

With these roles the host server is be able to create VMs using libvirtd utils, as virsh. The provision of those machines uses pxe boot to install a base distribution inside each VM. Then the vms.yml playbook apply the tasks and the roles spcified.

Provision virtual machines
--------------------------

The file vms.yml is only a base playbook, it provides pre and pro tasks and the roles to apply to the vms.

The destiny host of this playbook is a VM, but in order to create the VM before provision it some **pre-tasks** are defined in **includes/pre-tasks.yml**. Most of the tasks in this file are used to prepare the host and launch a VM. The file includes/post-tasks.yml is empty but it can be used to do some taks after the VM was ready, such create a node in the monitorin app or add a webserver to a balancing pool.

Other considerations
--------------------

As we can't reach the VMs ssh ports becouse the net is private, we must to tune SSH client in the machine where ansible is launched. The file ansible.cfg loads the ssh.cfg as every ssh comman used by Ansible. The ssh.cfg stablish a direct ssh connection to each VM using a tunnel created by **nc** tool. Only the host machine is accessed by a *normal* connection.


[ansible-ssh]:https://github.com/amatas/ansible-ssh
[ansible-utils]:https://github.com/amatas/ansible-utils
[ansible-libvirt]:https://github.com/amatas/ansible-libvirt
[ansible-pxe]:https://github.com/amatas/ansible-pxe
[ansible-iptables]:https://github.com/amatas/ansible-iptables
