## 15.4 使用 etcdctl

> **版本說明：** 本節示例基於 etcd 3.5 系列版本。請存取 [etcd 官方釋出頁](https://github.com/etcd-io/etcd/releases) 取得最新版本資訊。

`etcdctl` 是一個命令行客戶端，它能提供一些簡潔的命令，供使用者直接跟 `etcd` 服務打交道，而無需基於 `HTTP API` 方式。這在某些情況下將很方便，例如使用者對服務進行測試或者手動修改資料庫內容。我們也推薦在剛接觸 `etcd` 時透過 `etcdctl` 命令來熟悉相關的操作，這些操作跟 `HTTP API` 實際上是對應的。

`etcd` 專案二進位發行包中已經包含了 `etcdctl` 工具，沒有的話，可以從 [github.com/etcd-io/etcd/releases](https://github.com/etcd-io/etcd/releases) 下載。

`etcdctl` 支援如下的命令，大體上分為資料庫操作和非資料庫操作兩類，後面將分別進行解釋。

```bash
NAME:
	etcdctl - A simple command line client for etcd3.

USAGE:
	etcdctl

VERSION:
	3.5.29

API VERSION:
	3.5


COMMANDS:
	get			Gets the key or a range of keys
	put			Puts the given key into the store
	del			Removes the specified key or range of keys [key, range_end)
	txn			Txn processes all the requests in one transaction
	compaction		Compacts the event history in etcd
	alarm disarm		Disarms all alarms
	alarm list		Lists all alarms
	defrag			Defragments the storage of the etcd members with given endpoints
	endpoint health		Checks the healthiness of endpoints specified in `--endpoints` flag
	endpoint status		Prints out the status of endpoints specified in `--endpoints` flag
	watch			Watches events stream on keys or prefixes
	version			Prints the version of etcdctl
	lease grant		Creates leases
	lease revoke		Revokes leases
	lease timetolive	Get lease information
	lease keep-alive	Keeps leases alive (renew)
	member add		Adds a member into the cluster
	member remove		Removes a member from the cluster
	member update		Updates a member in the cluster
	member list		Lists all members in the cluster
	snapshot save		Stores an etcd node backend snapshot to a given file
	snapshot restore	Restores an etcd member snapshot to an etcd directory
	snapshot status		Gets backend snapshot status of a given file
	make-mirror		Makes a mirror at the destination etcd cluster
	migrate			Migrates keys in a v2 store to a mvcc store
	lock			Acquires a named lock
	elect			Observes and participates in leader election
	auth enable		Enables authentication
	auth disable		Disables authentication
	user add		Adds a new user
	user delete		Deletes a user
	user get		Gets detailed information of a user
	user list		Lists all users
	user passwd		Changes password of user
	user grant-role		Grants a role to a user
	user revoke-role	Revokes a role from a user
	role add		Adds a new role
	role delete		Deletes a role
	role get		Gets detailed information of a role
	role list		Lists all roles
	role grant-permission	Grants a key to a role
	role revoke-permission	Revokes a key from a role
	check perf		Check the performance of the etcd cluster
	help			Help about any command

OPTIONS:
      --cacert=""				verify certificates of TLS-enabled secure servers using this CA bundle
      --cert=""					identify secure client using this TLS certificate file
      --command-timeout=5s			timeout for short running command (excluding dial timeout)
      --debug[=false]				enable client-side debug logging
      --dial-timeout=2s				dial timeout for client connections
      --endpoints=[127.0.0.1:2379]		gRPC endpoints
      --hex[=false]				print byte strings as hex encoded strings
      --insecure-skip-tls-verify[=false]	skip server certificate verification
      --insecure-transport[=true]		disable transport security for client connections
      --key=""					identify secure client using this TLS key file
      --user=""					username[:password] for authentication (prompt if password is not supplied)
  -w, --write-out="simple"			set the output format (fields, json, protobuf, simple, table)
```

### 15.4.1 資料庫操作

資料庫操作圍繞鍵值和目錄的增刪改查（CRUD），覆蓋其完整生命週期管理。

etcd 在鍵的組織上採用了層次化的空間結構（類似於檔案系統中目錄的概念），使用者指定的鍵可以為單獨的名字，如 `testkey`，此時實際上位於根目錄 `/` 下面，也可以為指定目錄結構，如 `cluster1/node2/testkey`，則將建立相應的目錄結構。

> 注：CRUD 即 Create，Read，Update，Delete，是符合 REST 風格的一套 API 操作。

#### put

```bash
$ etcdctl put /testdir/testkey "Hello world"
OK
```

#### get

取得指定鍵的值。例如

```bash
$ etcdctl put testkey hello
OK
$ etcdctl get testkey
testkey
hello
```
支援的選項為

`--sort-by` 指定排序欄位（CREATE / KEY / MODIFY / VALUE / VERSION）

`--order` 指定排序順序（ASCEND / DESCEND）

`--consistency` 指定一致性級別（`l` 線性一致，`s` 序列）

#### del

刪除某個鍵值。例如

```bash
$ etcdctl del testkey
1
```

### 15.4.2 非資料庫操作

#### watch

監測一個鍵值的變化，一旦鍵值發生更新，就會輸出最新的值。

例如，使用者更新 `testkey` 鍵值為 `Hello world`。

```bash
$ etcdctl watch testkey
PUT
testkey
2
```

#### member

透過 `list`、`add`、`update`、`remove` 命令列出、加入、更新、刪除 etcd 例項到 etcd 集群中。

例如本地啟動一個 `etcd` 服務例項後，可以用如下命令進行查看。

```bash
$ etcdctl member list
422a74f03b622fef, started, node1, http://172.16.238.100:2380, http://172.16.238.100:2379
```
