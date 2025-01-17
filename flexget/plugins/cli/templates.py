from flexget import options
from flexget.event import event
from flexget.terminal import TerminalTable, TerminalTableError, console, table_parser
from flexget.utils.template import get_template, list_templates


def list_file_templates(manager, options):
    header = ['Name', 'Use with', 'Full Path', 'Contents']
    table_data = [header]
    console('Fetching all file templates, stand by...')
    for template_name in list_templates(extensions=['template']):
        if options.name and not options.name in template_name:
            continue
        template = get_template(template_name)
        if 'entries' in template_name:
            plugin = 'notify_entries'
        elif 'task' in template_name:
            plugin = 'notify_task'
        else:
            plugin = '-'
        name = template_name.replace('.template', '').split('/')
        if type(name) == list:
            if len(name) > 0:
                name = name[-1]
            else:
                name = '<ERR>'
        with open(template.filename) as contents:
            table_data.append([name, plugin, template.filename, contents.read()])

    try:
        table = TerminalTable(
            options.table_type, table_data, wrap_columns=[2, 3], drop_columns=[2, 3]
        )
    except TerminalTableError as e:
        console('ERROR: %s' % str(e))
    else:
        console(table.output)


@event('options.register')
def register_parser_arguments():
    parser = options.register_command(
        'templates',
        list_file_templates,
        help='View all available templates',
        parents=[table_parser],
    )
    parser.add_argument('--name', help='Filter results by template name')
