# Linux下对端口流量进行统计

在不修改源代码的情况下对程序暴露端口流量进行监控统计，可以利用Linux中自带的Iptable添加简单的规则让其起到端口流量统计的作用。但是需要注意的是在服务器重启、Iptable服务重启的时候统计数据会被重置清零。

## 添加需要统计的端口

### 1、输入监控

下面示例是监控目标端口是8080的输入流量 --dport(destination port 的缩写)

```bash
iptables -A INPUT -p tcp --sport 8080
```

### 2、输出监控

下面示例是监控来源端口是8080的输出流量 --sport(source port 的缩写)

```bash
iptables -A OUTPUT -p tcp --sport 8080
```

## 查看统计数据

```bash
iptables -L -v -n -x --line-numbers
```

示例结果：

8080端口接收的流量为2885字节，发送的流量是8240字节

```bash
Chain INPUT (policy ACCEPT 202 packets, 25187 bytes)
pkts bytes target prot opt in out source destination
18 2885 tcp -- * * 0.0.0.0/0 0.0.0.0/0 tcp dpt:8080

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
pkts bytes target prot opt in out source destination

Chain OUTPUT (policy ACCEPT 184 packets, 45774 bytes)
pkts bytes target prot opt in out source destination
12 8240 tcp -- * * 0.0.0.0/0 0.0.0.0/0 tcp spt:8080

```

## 重置统计数据

注意：这里是重置所有端口的统计数据

### 1、重置所有输入端口

```bash
Iptable -Z INPUT
```

### 2、重置所有输出端口

```bash
Iptable -Z OUTPUT
```

## 移除统计端口

### 1、移除输入端口

```bash
iptables -D INPUT -p tcp --dport 8080
```

### 2、移除输出端口

```bash
iptables -D OUTPUT -p tcp --sport 8080

```

[原博地址](https://www.jianshu.com/p/34e846b8b8ac)
