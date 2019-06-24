# Distributed KV with RabbitMQ Raft Library

This is a Distributed Key Value example based on [Ra](https://github.com/rabbitmq/ra).

## Requirements

* [rebar3](https://github.com/erlang/rebar3)

## Setup your env

```bash
wget https://s3.amazonaws.com/rebar3/rebar3 && chmod +x rebar3
```

## Compiling

``` bash
rebar3 compile
```

## Test the example in localhost:

To test the example in localhost with three nodes you can:

- run the node1:
```
rebar3 shell --sname node1
```

- run the node2:
```
rebar3 shell --sname node2

```
- run the node3:
```
rebar3 shell --sname node3
raft_kv:start_local().
```

Join the other nodes (node3):
```erlang
raft_kv:join(node2@GaS).
raft_kv:join(node1@GaS).
```

check the members:

```erlang
raft_kv_sm:members().
%% => Cluster Members:
%% => Leader:{kv,node3@GaS}
%% => Followers:[{kv,node1@GaS},{kv,node2@GaS}]
%% => Nodes:[{kv,node1@GaS},{kv,node2@GaS},{kv,node3@GaS}]
```

put values:
```erlang
(node3@GaS)5> raft_kv:put("key1","value1").
ok
(node3@GaS)6> raft_kv:put("key2","value1").
ok
(node3@GaS)7> raft_kv:put("key2","value2").
ok
(node3@GaS)8> raft_kv:put("key3","value3").
ok
```

get the values:
```erlang
(node1@GaS)1>  raft_kv:get("key1").
{ok,"value1"}
(node1@GaS)2>  raft_kv:get("key2").
{ok,"value2"}
(node1@GaS)3>  raft_kv:get("key3").
{ok,"value3"}
(node1@GaS)4>
```

you can test the failover by stopping a node
