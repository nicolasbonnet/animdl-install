import click

from ...config import SESSION_FILE
from ..helpers import sessions, to_stdout
from .download import animdl_download
from .stream import animdl_stream

def session_prompt(session_list):
    ts = lambda x: to_stdout(x, "animdl-session-search")
    ts("Found %d sessions(s)" % len(session_list))
    for n, anime in enumerate(session_list, 1):
        ts("[#%02d] %s" % (n, sessions.describe_session_dict(anime.get('stream_url'))))
    
    index = click.prompt("Select by the index (defaults to 1)", default=1, type=int, show_default=False) - 1
    
    if (index + 1) > len(session_list):
        ts("Applying modulus to get a valid index from incorrect index: #%02d -> #%02d" % (index + 1, index % len(session_list) + 1))
        index %= len(session_list)
    
    return session_list[index]

@click.command(name='continue', help="Continue your downloads or stream from where t'was left.")
@click.argument('name', required=False, default='')
@click.option('-v', is_flag=True, default=False, help="View the sessions that can be continued from.")
@click.pass_context
def animdl_continue(ctx: click.Context, name, v):
    """
    Just continue the stuff from where you left it (so that you won't have to type the same things all over again).
    
    By default, the most recent stream/download will be handed.
    """
    if v:
        _sessions = sessions.load_sessions(SESSION_FILE)
        for i, session in enumerate(_sessions, 1):
            to_stdout("[#%02d] %s" % (i, sessions.describe_session_dict(session)), 'animdl-continuation')
        if not _sessions:
            to_stdout('No active sessions found in the working directory.', 'animdl-continuation')
        return
    
    if name:
        ses = [*sessions.search_identifiers(SESSION_FILE, name)]
        
        if not len(ses):
            return to_stdout("No sessions of that identifier found.", 'animdl-continuation')
        
        session = session_prompt(ses)if len(ses) > 1 else ses.pop()
    else:
        session = sessions.get_most_recent_session(SESSION_FILE)
        if not session:
            return to_stdout("No recent session found in the working directory.", 'animdl-continuation')
    
    if session.get('type') == 'stream':
        return ctx.invoke(animdl_stream, **sessions.generate_stream_arguments(session))
    
    if session.get('type') == 'download':
        return ctx.invoke(animdl_download, **sessions.generate_download_arguments(session))