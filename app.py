from __future__ import print_function
import libvirt
import sys
import os


#Menus
def menuPrincipal():
    print()
    choice = raw_input("0: Hypervisor machine name\n1: List stopped virtual machines\n2: List active virtual machines\n3: Start a machine\n4: Stop a machine\n5: Show a machine\n6: IP address of a machine\n7: Quit\n\nPlease enter your choice: ")

    if choice == "0":
        hypervisorName()
    elif choice == "1":
        listStoppedMachines()
    elif choice == "2":
        listActiveMachines()
    elif choice == "3":
        startMachine()
    elif choice == "4":
        stopMachine()
    elif choice == "5":
        showMachine()
    elif choice == "6":
        addrMachine()
    elif choice == "7":
        conn.close()
        sys.exit
    else:
        print("Invalid number")
        resume()


#Features
def hypervisorName():
    print()
    host = conn.getHostname()
    print('Hostname : '+host)
    print()
    resume()

def listStoppedMachines():
    print()
    if len(conn.listDefinedDomains()) == 0:
        print('No stopped virtual machine')
    else:
        print('Stopped machines : ')
        print(conn.listDefinedDomains())
    print()
    resume()

def listActiveMachines():
    print()
    domainIDs = conn.listDomainsID()
    if domainIDs == None:
        print('Failed to get a list of domain IDs', file=sys.stderr)
    if len(domainIDs) == 0:
        print('No active virtual machine ')
    else:
        print('Active machines : ')
        for domainID in domainIDs:
            domain = conn.lookupByID(domainID)
            print(domain.name(),' ')
    print()
    resume()

def startMachine():
    print()
    if len(conn.listDefinedDomains()) == 0:
        print('No stopped virtual machine')
        print()
    else:
        print('Stopped machines : ')
        for i in range(0,len(conn.listDefinedDomains())):
            print (i,": ",conn.listDefinedDomains()[i])
        num = input("Which machine do u want to start? Enter number ")
        if (num < len(conn.listDefinedDomains())):
            vm = conn.lookupByName(conn.listDefinedDomains()[num])
            vm.create()
            print("The VM has been successfully started")
            print()
    resume()

def stopMachine():
    print()
    print("Active virtual machines : ")
    domainIDs = conn.listDomainsID()
    if domainIDs == None:
        print('Failed to get a list of domain IDs', file=sys.stderr)
    if len(domainIDs) == 0:
        print('No active virtual machine ')
        print()
    else:
        for domainID in domainIDs:
            domain = conn.lookupByID(domainID)
            print(domainID,': ', domain.name())
        num = input("Which machine do u want to stop? Enter ID ")
        if num in domainIDs:
            domain = conn.lookupByID(num)
            vm = conn.lookupByName(domain.name())
            vm.destroy()
            print("The VM has been successfully stopped")
            print()
    resume()

def addrMachine():
    print()
    print("Active virtual machines : ")
    domainIDs = conn.listDomainsID()
    if domainIDs == None:
        print('Failed to get a list of domain IDs', file=sys.stderr)
    if len(domainIDs) == 0:
        print('No active virtual machine ')
        print()
    else:
        for domainID in domainIDs:
            domain = conn.lookupByID(domainID)
            print(domainID,': ', domain.name())
        num = input("Which machine do u want to show its interface address ? Enter ID ")
        if num in domainIDs:
            domain = conn.lookupByID(num)
            vm = conn.lookupByName(domain.name())
            ifaces = vm.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
            print("The interface IP addresses:")
            for (name, val) in ifaces.iteritems():
                if val['addrs']:
                    for ipaddr in val['addrs']:
                        if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                            print(ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV4")
                        elif ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV6:
                            print(ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV6")
                print()
    resume()

def showMachine():
    print()
    print("Active virtual machines : ")
    domainIDs = conn.listDomainsID()
    if domainIDs == None:
        print('Failed to get a list of domain IDs', file=sys.stderr)
    if len(domainIDs) == 0:
        print('No active virtual machine ')
        print()
    else:
        for domainID in domainIDs:
            domain = conn.lookupByID(domainID)
            print(domainID,': ', domain.name())
        num = input("Which machine do u want to show? Enter ID ")
        if num in domainIDs:
            domain = conn.lookupByID(num)
            os.system("virt-viewer "+ domain.name()+ " &")
            print()
    resume()

def resume():
    resumeVar = raw_input("Continue ? (y/n) ")
    if resumeVar == "y":
        os.system('clear')
        menuPrincipal()
    else:
        sys.exit

#MAIN
conn = libvirt.open('qemu:///system')
if conn == None:  
    print('Connexion failed',file=sys.stderr)
    exit(1)
menuPrincipal()
