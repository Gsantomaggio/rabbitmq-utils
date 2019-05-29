%%%-------------------------------------------------------------------
%% @doc raft_kv top level supervisor.
%% @end
%%%-------------------------------------------------------------------

-module(raft_kv_sup).

-behaviour(supervisor).

%% API
-export([start_link/0]).

%% Supervisor callbacks
-export([init/1]).

-define(SERVER, ?MODULE).

%%====================================================================
%% API functions
%%====================================================================

start_link() ->
  supervisor:start_link({local, ?SERVER}, ?MODULE, []).

%%====================================================================
%% Supervisor callbacks
%%====================================================================

%% Child :: #{id => Id, start => {M, F, A}}
%% Optional keys are restart, shutdown, type, modules.
%% Before OTP 18 tuples must be used to specify a child. e.g.
%% Child :: {Id,StartFunc,Restart,Shutdown,Type,Modules}
init([]) ->
  RestartStrategy = {one_for_one, 10, 60},
  ChildSpec = [{raft_kv, {raft_kv, start_link, []},
    permanent, brutal_kill, worker, [raft_kv]}],

  {ok, {RestartStrategy, ChildSpec}}.
%%====================================================================
%% Internal functions
%%====================================================================
