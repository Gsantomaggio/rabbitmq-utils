%%%-------------------------------------------------------------------
%%% @author gabriele
%%% @copyright (C) 2019, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 29. May 2019 11.32
%%%-------------------------------------------------------------------
-module(raft_kv_sm).
-behaviour(ra_machine).
-author("gabriele").


%% API
-export([init/1, apply/3, write/3, read/2, start_cluster/2, members/0,
  members/1, start_local_server/2, start_and_join/2]).

-record(?MODULE, {kvstore = #{} :: map()}).


init(_) ->
  #?MODULE{}.


apply(_Meta, {write, Key, Value}, #?MODULE{kvstore = KvM} = State) ->
  KvM0 = maps:put(Key, Value, KvM),
  {State#?MODULE{kvstore = KvM0}, ok, []};
apply(_Meta, {read, Key}, #?MODULE{kvstore = KvM} = State) ->
  Reply = maps:get(Key, KvM, undefined),
  {State, Reply, []};
apply(#{index := Idx}, _, State) ->
  %% notify all watchers of the change of value
  Effects = case Idx rem 1000 of
              0 -> [{release_cursor, Idx, State}];
              _ -> []
            end,
  {State, ok, Effects};
apply(_Meta, {nodedown, _}, State) ->
  %% we need to handle the nodedown as well to avoid crashing
  {State, ok, []}.


write(Server, Key, Value) ->
  case ra:process_command(Server, {write, Key, Value}) of
    {ok, _, _} ->
      ok;
    Err ->
      Err
  end.

read(Server, Key) ->
  case ra:process_command(Server, {read, Key}) of
    {ok, Value, _} ->
      {ok, Value};
    Err ->
      Err
  end.

start_cluster(Name, Node) ->
  ra:start_cluster(Name, {module, ?MODULE, #{}}, [{kv, Node}]).

start_local_server(Name, Node) ->
  ra:start_server(Name, {kv, Node}, {module, ?MODULE, #{}}, []),
  ok = ra:trigger_election({kv, Node}).


start_and_join(Name, New) ->
  ServerRef = {kv, node()},
  {ok, _, _} = ra:add_member(ServerRef, {kv, New}),
  ok = ra:start_server(Name, {kv, New}, {module, ?MODULE, #{}}, [ServerRef]),
  ok.


members() ->
  members(node()).

members(Node) ->
  case ra:members({kv, Node}) of
    {ok, Result, Leader} -> io:format("Cluster Members:~nLeader:~p~nFollowers:~p~n" ++
    "Nodes:~p~n", [Leader, lists:delete(Leader, Result), Result]);
    Err -> io:format("Cluster Status error: ~p", [Err])
  end.
