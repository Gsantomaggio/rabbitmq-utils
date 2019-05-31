%%%-------------------------------------------------------------------
%%% @author gabriele
%%% @copyright (C) 2019, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 29. May 2019 11.28
%%%-------------------------------------------------------------------
-module(raft_kv).
-author("gabriele").

-behaviour(gen_server).


%% API
-export([start_link/0, callback_mode/0, start_cluster/1,
  members/0, start_local/0, join/1, get/1, put/2]).

%% gen_server callbacks
-export([init/1,
  handle_call/3,
  handle_cast/2,
  handle_info/2,
  terminate/2,
  code_change/3]).

-define(SERVER, ?MODULE).
-define(NAME, "KV Raft Cluster").


-record(state, {}).

%%%===================================================================
%%% API
%%%===================================================================

%%--------------------------------------------------------------------
%% @doc
%% Starts the server
%%
%% @end
%%--------------------------------------------------------------------
-spec(start_link() ->
  {ok, Pid :: pid()} | ignore | {error, Reason :: term()}).
start_link() ->
  gen_server:start_link({local, ?SERVER}, ?MODULE, [], []).

init([]) ->
  io:format("Starting"),
  {ok, #state{}}.

callback_mode() ->
  handle_event_function.


handle_call({startlocal}, _From, State) ->
  R = raft_kv_sm:start_cluster(?NAME, node()),
  {reply, R, State};
handle_call({join, Node}, _From, State) ->
  R = raft_kv_sm:start_and_join(?NAME, Node),
  {reply, R, State};
handle_call({write, Key, Value}, _From, State) ->
  R = raft_kv_sm:write({kv, node()}, Key, Value),
  {reply, R, State};
handle_call({read, Key}, _From, State) ->
  R = raft_kv_sm:read({kv, node()}, Key),
  {reply, R, State};
handle_call({members, Node}, _From, State) ->
  raft_kv_sm:members(Node),
  {reply, ok, State}.


handle_cast(_Request, State) ->
  {noreply, State}.

handle_info(_Info, State) ->
  {noreply, State}.

terminate(_Reason, _State) ->
  ok.

code_change(_OldVsn, State, _Extra) ->
  {ok, State}.


%%%%%%%%%%%%

start_cluster(Name) ->
  gen_statem:call(?MODULE, {start, Name, node()}).

start_local() ->
  gen_statem:call(?MODULE, {startlocal}).

join(Node) ->
  gen_statem:call(?MODULE, {join, Node}).

put(Key, Value) ->
  gen_statem:call(?MODULE, {write, Key, Value}).

get(Key) ->
  gen_statem:call(?MODULE, {read, Key}).


members() ->
  gen_statem:call(?MODULE, {members, node()}).


