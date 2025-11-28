# This file is part of SAGE Education.   The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields, Unique, Check
from trytond.pyson import Eval, Not, Bool
from trytond.pool import Pool
from sql.aggregate import Sum
from trytond.exceptions import UserError
from trytond.transaction import Transaction
from datetime import date

#from .variables import _COURSE_YEAR
_COURSE_YEAR = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
)


class LectiveYear(ModelSQL, ModelView):
    'Lective Year'
    __name__ ='akademy_configuration.lective.year'

    code = fields.Char('Código', size=20,
        help="Código do ano letivo.\nEx: 22/23")
    name = fields.Char('Nome', required=True, 
        help="Nome do ano letivo.")
    start = fields.Date('Início', required=True,          
        help="Data de início do ano letivo.")
    end = fields.Date('Término', required=True, 
        help="Data de término do ano letivo.")
    description = fields.Text('Descrição')
    classes = fields.One2Many('akademy_classe.classes', 
        'lective_year', 'Turma')
    quarter = fields.One2Many('akademy_configuration.quarter', 
        'lective_year', 'Períodos letivos')
    studyplan = fields.One2Many('akademy_configuration.studyplan', 
        'lective_year', 'Plano de estudo')

    @classmethod
    def __setup__(cls):
        super(LectiveYear, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name),
            u'Não foi possível cadastrar o novo ano letivo, por favor verificar se o nome inserido já existe.'),
            ('code', Unique(table, table.code),
            u'Não foi possível cadastrar o novo ano letivo, por favor verificar se o código inserido já existe.'),
            ('start_date', Check(table, table.start < table.end),
            u'Não foi possível cadastrar o novo ano letivo, por favor verificar se a data de início é menor que a data de término.')
        ]
        cls._order = [('name', 'ASC')]

    '''
    @classmethod
    def delete(cls, lective_years):
        for lective_year in lective_years:            
            if len(lective_year.classes) < 1:
                super(LectiveYear, cls).delete(lective_year)
            else:
                raise UserError("Não foi possível eliminar o ano letivo, por favor verificar se o mesmo já tem uma turma associada.")	
    '''
    
    @classmethod
    def default_start(cls):
        return date.today()


class Quarter(ModelSQL, ModelView):
    'Quarter'
    __name__ = 'akademy_configuration.quarter'
    
    code = fields.Char('Código', size=20,
        help="Código do período letivo.\nEx: 1º Trimestre")
    name = fields.Char('Nome', required=True, 
        help="Nome do período letivo.")
    start = fields.Date('Início', required=True,          
        help="Data de início do período letivo.")
    end = fields.Date('Término', required=True, 
        help="Data de término do período letivo.")
    description = fields.Text('Descrição')
    lective_year = fields.Many2One(
		'akademy_configuration.lective.year', 'Ano letivo', 
		required=True, ondelete="RESTRICT",
		help="Nome do ano letivo.")
    studyplan_discipline = fields.One2Many(
		'akademy_configuration.studyplan.discipline', 'quarter', 
		'Disciplina')
    studyplan_avaliations = fields.One2Many(
		'akademy_configuration.studyplan.avaliation', 'quarter', 
		'Avaliação')

    @classmethod
    def __setup__(cls):
        super(Quarter, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name, table.lective_year),
            u'Não foi possível cadastrar o novo período letivo, por favor verificar se o nome inserido já existe.'),
            ('start_date', Check(table, table.start < table.end),
            u'Não foi possível cadastrar o novo período letivo, por favor verificar se a data de início é menor que a data de término.')
        ]

    @classmethod
    def default_start(cls):
        return date.today()


class TimeCourse(ModelSQL, ModelView):
    'Time Course'
    __name__ = 'akademy_configuration.time.course'

    code = fields.Char('Código', size=20,
        help="Código do período.")
    name = fields.Char('Período', required=True, 
        help="Nome do período.")
    description = fields.Text('Descrição')        
    start_time = fields.Time('Entrada', format='%H:%M',
        required=True, help=u'Hora de início da aula.')
    end_time = fields.Time('Saída', format='%H:%M', 
        required=True, help=u'Hora de término da aula.')
    classes = fields.One2Many(
        'akademy_classe.classes', 'time_course', 'Turma')

    @classmethod
    def __setup__(cls):
        super(TimeCourse, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name, table.code),
            u'Não foi possível cadastrar o novo período letivo, por favor verificar se o nome ou o código inserido já existe.'),            
            ('start_time', Check(table, table.start_time < table.end_time),
            u'Não foi possível cadastrar o novo período letivo, por favor verificar se a hora de entrada é menor que a hora de saída.')
        ]
        cls._order = [('name', 'ASC')]


class Classe(ModelSQL, ModelView):
    'Classe'
    __name__ = 'akademy_configuration.classe'    

    code = fields.Char('Código', size=20,
        help="Código da classe.\nEx: Classe-7")
    name = fields.Char('Nome', required=True, 
        help="Nome da classe.")
    description = fields.Text('Descrição')
    course_classe = fields.One2Many('akademy_configuration.course.classe', 
        'classe', 'Curso')
    classes = fields.One2Many('akademy_classe.classes', 
        'classe', 'Turma')
    student = fields.One2Many('company.student', 
        'classe', 'Discente')

    @classmethod
    def __setup__(cls):
        super(Classe, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name),
            u'Não foi possível cadastrar a nova classe, por favor verificar se o nome inserido já existe.'),
            ('code', Unique(table, table.code),
            u'Não foi possível cadastrar a nova classe, por favor verificar se o código inserido já existe.')            
        ]
        cls._order = [('name', 'ASC')]


class ClasseTimeType(ModelSQL, ModelView):
    "Classe Time - Type"
    __name__ = 'akademy_configuration.classe.time.type'
    
    name = fields.Char('Nome', required=True,
        help="Nome do tempo letivo.\nEx: 1º Tempo")
    classe_time_rule = fields.One2Many('akademy_classe.classe.timerule', 
        'lesson_time', 'Horário')
    classe_teacher_lesson = fields.One2Many('akademy_classe.classe.teacher.lesson', 
        'lesson_type', 'Plano de aula')

    @classmethod
    def __setup__(cls):
        super(ClasseTimeType, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name),
            u'Não foi possível cadastrar o novo tempo letivo, por favor verificar se o nome inserido já existe.')
        ]


class MatriculationType(ModelSQL, ModelView):
    "Matriculation Type"
    __name__ = 'akademy_configuration.matriculation.type'

    name = fields.Char('Nome', required=True,
        help="Nome do tipo da matrícula.\nEx: Candidato, Transfêrido(a), Mudança de turma")
    classe_student = fields.One2Many('akademy_classe.classe.student', 
        'type', 'Tipo de matrícula')

    @classmethod
    def __setup__(cls):
        super(MatriculationType, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name),
            u'Não foi possível cadastrar o novo tipo de matrícula, por favor verificar se o nome inserido já existe.')
        ]

    @classmethod
    def matriculation_type(cls, type):
        matriculation_type = MatriculationType.search([
            ('name', '=', type)
            ])
        
        if len(matriculation_type) > 0:
            return matriculation_type[0]
        return None


class MatriculationState(ModelSQL, ModelView):
    "Matriculation State"
    __name__ = 'akademy_configuration.matriculation.state'

    name = fields.Char('Nome', required=True,
        help="Nome do estado da matrícula.\nEx: Matrículado(a), Transfêrido(a)")
    access = fields.Boolean('Acesso', 
        help="A este estado é permite o acesso.")
    student = fields.One2Many('company.student', 'state', 
        'Estado de matrícula')
    classe_student = fields.One2Many('akademy_classe.classe.student', 
        'state', 'Estado de matrícula')
    classe_student_discipline = fields.One2Many('akademy_classe.classe.student.discipline', 
        'state', 'Estado de matrícula')
    classe_teacher = fields.One2Many('akademy_classe.classe.teacher', 
        'state', 'Estado de matrícula')
    classe_teacher_discipline = fields.One2Many('akademy_classe.classe.teacher.discipline', 
        'state', 'Estado de matrícula')

    @classmethod
    def __setup__(cls):
        super(MatriculationState, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name),
            u'Não foi possível cadastrar o novo estado de matrícula, por favor verificar se o nome inserido já existe.')
        ]


class Discipline(ModelSQL, ModelView):
    'Discipline'
    __name__ = 'akademy_configuration.discipline'

    code = fields.Char('Código', size=20,
        help="Código da disciplina.")
    name = fields.Char('Nome', required=True, 
        help="Nome da disciplina.")
    lesson_type = fields.Many2One('akademy_configuration.classe.lesson.type', 
        'Aula', required=True, help="Escolha o tempo de aula.")	
    description = fields.Text('Descrição')
    studyplan_discipline = fields.One2Many('akademy_configuration.studyplan.discipline', 
        'discipline', 'Disciplina')
    discipline_precentes = fields.One2Many('akademy_configuration.discipline.precedents', 
        'discipline', 'Disciplina antecedentes')  

    @classmethod
    def __setup__(cls):
        super(Discipline, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints += [
            ('code', Unique(table, table.name),
            u'Não foi possível cadastrar a nova disciplina, por favor verificar se o nome inserido já existe.')
        ]
        cls._order = [('name', 'ASC')]

    @classmethod
    def default_lesson_teoric(cls):
        return True


class DisciplineModality(ModelSQL, ModelView):
    "Discipline Modality Frequence"
    __name__ = 'akademy_configuration.discipline.modality'

    name = fields.Char('Nome', required=True,
        help="Nome da modalidade de frequência da disciplina.\nEx: Presencial, Virtual")
    studyplan_discipline = fields.One2Many('akademy_configuration.studyplan.discipline', 
        'modality', 'Modalidade de frequência')
    classes = fields.One2Many('akademy_classe.classes', 
        'modality', 'Modalidade de frequência')
    classe_student_discipline = fields.One2Many('akademy_classe.classe.student.discipline', 
        'modality', 'Modalidade de frequência')
    classe_teacher_discipline = fields.One2Many('akademy_classe.classe.teacher.discipline', 
        'modality', 'Modalidade de frequência')

    @classmethod
    def __setup__(cls):
        super(DisciplineModality, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name),
            u'Não foi possível cadastrar a nova modalidade frequência da disciplina, por favor verificar se o nome inserido já existe.')
        ]  


class DisciplineState(ModelSQL, ModelView):
    "Discipline State Frequence"
    __name__ = 'akademy_configuration.discipline.state'

    name = fields.Char('Nome', required=True,
        help="Nome do estado de frequência da disciplina.\nEx: Obrigatório, Opcional")
    required = fields.Boolean('Obrigatório', 
        help="Este estado é de caráter obrigatório.")
    studyplan_discipline = fields.One2Many('akademy_configuration.studyplan.discipline', 
        'state', 'Estado de frequência')
    studyplan_avaliation = fields.One2Many('akademy_configuration.studyplan.avaliation', 
        'state', 'Estado de frequência')

    @classmethod
    def __setup__(cls):
        super(DisciplineState, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name),
            u'Não foi possível cadastrar o novo estado de frequência da disciplina, por favor verificar se o nome inserido já existe.')
        ]


class DisciplinePrecedents(ModelSQL, ModelView):
    'Discipline Precedents'
    __name__ = 'akademy_configuration.discipline.precedents'
    
    discipline = fields.Many2One('akademy_configuration.discipline', 
        'Disciplina', required=True, ondelete="RESTRICT")   
    studyplan_discipline = fields.Many2One('akademy_configuration.studyplan.discipline', 
        'Disciplina', ondelete="RESTRICT") 
    grade = fields.Numeric(string=u'Nota', digits=(2,1))

    @classmethod
    def __setup__(cls):
        super(DisciplinePrecedents, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('discipline', Unique(table, table.discipline, table.studyplan_discipline),
            u'Não foi possível cadastrar a disciplina, por favor verificar se a disciplina inserida já existe.')            
        ]

    @classmethod
    def default_grade(cls):
        return 0 

    def get_rec_name(self, name):
        t1 = '%s' % \
            (self.discipline.rec_name)
        return t1

    @classmethod
    def search_rec_name(cls, name, clause):
        return [('discipline.rec_name',) + tuple(clause[1:])] 


class ClasseLessonType(ModelSQL, ModelView):
    "Classe Lesson - Type"
    __name__ = 'akademy_configuration.classe.lesson.type'

    name = fields.Char('Nome', required=True,
        help="Nome do tipo de aula.\nEx: Teórica, Prática")
    discipline = fields.One2Many('akademy_configuration.discipline', 
        'lesson_type', 'Disciplina')
    classe_room = fields.One2Many('akademy_configuration.classe.room', 
        'lesson_type', 'Sala de aula')

    @classmethod
    def __setup__(cls):
        super(ClasseLessonType, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name),
            u'Não foi possível cadastrar o novo tipo de aula, por favor verificar se o nome inserido já existe.')
        ]  


class ClasseRoom(ModelSQL, ModelView):
    'Classe Room'
    __name__ = 'akademy_configuration.classe.room'

    code = fields.Char('Código', size=20,
        help="Código da sala de aula.")
    name = fields.Char('Nome', required=True,
        help="Nome da sala de aula.")    
    lesson_type = fields.Many2One('akademy_configuration.classe.lesson.type', 
        'Aula', required=True, ondelete="RESTRICT",
        help="Escolha o tipo de aula.")	
    capacity = fields.Integer('Capacidade',
        help="Capacidade máxima da sala de aula.")
    description = fields.Text('Descrição')

    @classmethod
    def __setup__(cls):
        super(ClasseRoom, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name),
            u'Não foi possível cadastrar a nova sala de aula, por favor verificar se o nome inserido já existe.'),
            ('capacity', Check(table, table.capacity > 0),
            u'Não foi possível cadastrar a nova sala de aula, por favor verifica a capacidade.')            
        ] 
        cls._order = [('name', 'ASC')] 

    @classmethod
    def default_capacity(cls):
        return 35


class AcademicLevel(ModelSQL, ModelView):
    'Academic Level'
    __name__ = 'akademy_configuration.academic.level'

    code = fields.Char('Código', size=20,
        help="Código do nível académico.")
    name = fields.Char('Nome', required=True, 
        help="Nome do nível académico.")
    description = fields.Text('Descrição')
    area = fields.One2Many('akademy_configuration.area', 
        'academic_level', 'Área')
    studyplan = fields.One2Many('akademy_configuration.studyplan', 
        'academic_level', 'Plano de estudo')
    student = fields.One2Many('company.student', 
        'academic_level', 'Discente')

    @classmethod
    def __setup__(cls):
        super(AcademicLevel, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name, table.code),
            u'Não foi possível cadastrar o novo nível académico, por favor verificar se o nome ou o código inserido já existe.')
        ]
        cls._order = [('name', 'ASC')]


class Area(ModelSQL, ModelView):
    'Area'
    __name__ = 'akademy_configuration.area'    

    code = fields.Char('Código', size=20,
        help="Código da área.")
    name = fields.Char('Nome', required=True, 
        help="Nome da área.")
    description = fields.Text('Descrição')
    academic_level  = fields.Many2One('akademy_configuration.academic.level', 
        'Nível académico', ondelete="RESTRICT") 
    studyplan = fields.One2Many('akademy_configuration.studyplan', 
        'area', 'Plano de estudo')
    course = fields.One2Many('akademy_configuration.course', 
        'area', 'Curso', required=True)
    company_student = fields.One2Many('company.student', 
        'area', 'Discente')  

    @classmethod
    def __setup__(cls):
        super(Area, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name, table.code),
            u'Não foi possível cadastrar a nova área, por favor verificar se o nome ou o código inserido já existe.')
        ]
        cls._order = [('name', 'ASC')]
 

class Course(ModelSQL, ModelView):
    'Course'    
    __name__ = 'akademy_configuration.course'

    code = fields.Char('Código', size=20,
        help="Código do curso.")
    name = fields.Char('Nome', required=True, 
        help="Nome do curso.")
    duration = fields.Selection(selection=_COURSE_YEAR,
        string=u'Duração', required=True,
        help="Escolha a duração do curso em anos.")
    description = fields.Text('Descrição')        
    area = fields.Many2One('akademy_configuration.area', 
        'Área', ondelete="RESTRICT")
    course_classe = fields.One2Many('akademy_configuration.course.classe', 
        'course', 'Classe', required=True)
    studyplan = fields.One2Many('akademy_configuration.studyplan', 
        'course', 'Plano de estudo')
    company_student = fields.One2Many('company.student', 
        'area', 'Discente') 

    @classmethod
    def __setup__(cls):
        super(Course, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name, table.code),
            u'Não foi possível cadastrar o novo curso, por favor verificar se o nome ou o código inserido já existe.')
        ]
        cls._order = [('name', 'ASC')]


class CourseClasse(ModelSQL, ModelView):
    'Course Classe'
    __name__ = 'akademy_configuration.course.classe'
    
    description = fields.Text('Descrição')
    course_year = fields.Selection(selection=_COURSE_YEAR,
        string=u'Ano', required=True,
        help="Escolha o ano do curso.")
    classe = fields.Many2One('akademy_configuration.classe', 
        'Classe', required=True, ondelete="RESTRICT")
    course = fields.Many2One('akademy_configuration.course', 
        'Curso', required=True, ondelete="RESTRICT")
    studyplan = fields.One2Many('akademy_configuration.studyplan', 
        'classe', 'Plano de estudo')      

    @classmethod
    def __setup__(cls):
        super(CourseClasse, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('classe', Unique(table, table.classe, table.course),
            u'Não foi possível associar a classe ao curso, por favor verificar se classe e o curso já não se encontram associados.')            
        ]
        cls._order = [('classe.name', 'ASC')]

    def get_rec_name(self, name):
        t1 = '%s' % \
            (self.classe.rec_name)
        return t1

    @classmethod
    def search_rec_name(cls, name, clause):
        return [('classe.rec_name',) + tuple(clause[1:])] 


class MetricAvaliation(ModelSQL, ModelView):
    'Metric Avaliation'
    __name__ = 'akademy_configuration.metric.avaliation'
 
    name = fields.Char('Nome', required=True,
        help="Nome da métrica que corresponde a avaliação.")    
    avaliation = fields.Many2One('akademy_configuration.avaliation', 
        'Avaliação', required=True, ondelete='CASCADE')  
    avaliation_type = fields.Many2One('akademy_configuration.avaliation.type', 
        'Tipo de avaliação', required=True, ondelete='CASCADE') 
    studyplan_avaliation = fields.One2Many('akademy_configuration.studyplan.avaliation', 
        'metric_avaliation', 'Avaliações')

    @classmethod
    def __setup__(cls):
        super(MetricAvaliation, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('key', Unique(table, table.name),
            u'Não foi possível cadastrar a nova métrica, por favor verificar se o nome inserido já existe.')
        ]
        cls._order = [('name', 'ASC')]


class Avaliation(ModelSQL, ModelView):
    'Avaliation'
    __name__ = 'akademy_configuration.avaliation'
    
    name = fields.Char('Nome', required=True,
        help="Nome da avaliação.")
    description = fields.Text('Descrição')     
    metric_avaliation = fields.One2Many('akademy_configuration.metric.avaliation', 
        'avaliation', 'Avaliação')    

    @classmethod
    def __setup__(cls):
        super(Avaliation, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name),
            u'Não foi possível cadastrar a nova avaliação, por favor verificar se o nome inserido já existe para esta métrica.')
        ]
    
 
class AvaliationType(ModelSQL, ModelView):
    'Avaliation Type'
    __name__ = 'akademy_configuration.avaliation.type'
    
    name = fields.Char('Nome', required=True, 
        help="Nome do tipo de avaliação.")
    description = fields.Text('Descrição')      
    metric_avaliation = fields.One2Many('akademy_configuration.metric.avaliation', 
        'avaliation_type', 'Tipo de avaliação') 

    @classmethod
    def __setup__(cls):
        super(AvaliationType, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name', Unique(table, table.name),
            u'Não foi possível cadastrar o novo tipo de avaliação, por favor verificar se o nome inserido já existe para esta métrica.')
        ]


class StudyPlan(ModelSQL, ModelView):
    'StudyPlan'
    __name__ = 'akademy_configuration.studyplan'
    
    code = fields.Char('Código', size=25,
        help="Código do plano de estudo.")    
    name = fields.Char('Nome', required=True,
        help="Nome do plano de estudo.")
    lective_year = fields.Many2One('akademy_configuration.lective.year', 
        'Ano letivo', required=True, ondelete="RESTRICT")    
    academic_level = fields.Many2One('akademy_configuration.academic.level', 
        'Nível académico', required=True, ondelete="RESTRICT")
    area = fields.Many2One('akademy_configuration.area', 'Área', 
        domain=[('academic_level', '=', Eval('academic_level', -1))],
        depends=['academic_level'], required=True, ondelete="RESTRICT")
    course = fields.Many2One('akademy_configuration.course', 'Curso', 
        domain=[('area', '=', Eval('area', -1))],
        depends=['area'], required=True, ondelete="RESTRICT")
    classe = fields.Many2One('akademy_configuration.course.classe', 'Classe', 
        domain=[('course', '=', Eval('course', -1))],
        depends=['course'], required=True, ondelete="RESTRICT")
    studyplan_discipline = fields.One2Many('akademy_configuration.studyplan.discipline', 
        'studyplan', 'Disciplina')
    classes = fields.One2Many('akademy_classe.classes', 'studyplan', 'Turma')
    hours_per_corse = fields.Function(
        fields.Numeric(
            string=u'Total de horas', readonly=True), 
        'get_hours_per_corse', searcher='search_hours_per_corse')

    @classmethod
    def __setup__(cls):
        super(StudyPlan, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('Key', Unique(table, table.name, table.code, table.classe),
            u'Não foi possível cadastrar o novo plano de estudo, por favor verificar se o nome ou código inserido já existe.')            
        ]
        cls._order = [('classe.classe.name', 'ASC')]

    '''
    @classmethod
    def delete(cls, studyplans):
        for studyplan in studyplans:            
            if len(studyplan.classes) < 1:
                super(StudyPlan, cls).delete(studyplan)
            else:
                raise UserError("Não foi possível eliminar o plano de estudo, por favor verificar se o mesmo já tem uma turma associada.")	
    '''
    
    @classmethod
    def get_hours_per_corse_sql(cls):
        """ get sql-code for 'get_hours_per_corse'
        """
        StudyPlanDiscipline = Pool().get('akademy_configuration.studyplan.discipline')
        tab_spd = StudyPlanDiscipline.__table__()
        tab_sp = cls.__table__()
        
        qu1 = tab_spd.join(tab_sp, condition=tab_spd.studyplan==tab_sp.id
            ).select(tab_sp.id.as_('id_model'),
                Sum(
                    tab_spd.hours
                ).as_('hours_course'),
                group_by=[tab_sp.id],
            )
        return qu1

    @classmethod
    def get_hours_per_corse(cls, studyplans, names):
        """ get hours per week
        """
        r1 = {'hours_per_corse': {}}
        tab_hours = cls.get_hours_per_corse_sql()
        cursor = Transaction().connection.cursor()
        id_lst = [x.id for x in studyplans]
                
        for i in id_lst:
            r1['hours_per_corse'][i] = 0
        
        qu1 = tab_hours.select(tab_hours.id_model,
                tab_hours.hours_course,
                where=tab_hours.id_model.in_(id_lst)
            )
        cursor.execute(*qu1)
        l1 = cursor.fetchall()
        for i in l1:
            (id1, h1) = i
            r1['hours_per_corse'][id1] = h1

        return r1
        
    @classmethod
    def search_hours_per_corse(cls, name, clause):
        """ search in hour/week
        """
        tab_hours = cls.get_hours_per_corse_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]

        qu1 = tab_hours.select(tab_hours.id_model,
                where=Operator(tab_hours.hours_course, clause[2])
            )
        return [('id', 'in', qu1)]


class StudyPlanDiscipline(ModelSQL, ModelView):
    'StudyPlan Discipline'
    __name__ = 'akademy_configuration.studyplan.discipline'
      
    description = fields.Text('Descrição')    
    state = fields.Many2One('akademy_configuration.discipline.state', 
        'Estado', required=True, help="Escolha o estado de frequência.")
    modality = fields.Many2One('akademy_configuration.discipline.modality', 
        'Modalidade', required=True, help="Escolha a modalidade de frequência.")
    quarter = fields.Many2One('akademy_configuration.quarter', 'Período letivo', 
        required=True, ondelete="RESTRICT",
        help="Escolha o período letivo em que a disciplina será lecionada.")      
    hours = fields.Integer('Total de horas', required=True,
        help="Carga horária da disciplina.")
    flaut = fields.Integer('Total de faltas', required=True,
        help="Número máximo de faltas.")
    average = fields.Numeric('Média', digits=(2,2), 
        required=True, help='Média para aprovação.')
    studyplan = fields.Many2One('akademy_configuration.studyplan', 'Plano de estudo',
        ondelete="RESTRICT")
    discipline = fields.Many2One('akademy_configuration.discipline', 
        'Disciplina', required=True, ondelete="RESTRICT")
    studyplan_avaliations = fields.One2Many('akademy_configuration.studyplan.avaliation', 
        'studyplan_discipline', 'Avaliações')
    discipline_precedentes = fields.One2Many('akademy_configuration.discipline.precedents', 
        'studyplan_discipline', 'Disciplina precedentes')
    classe_student_discipline = fields.One2Many('akademy_classe.classe.student.discipline', 
        'studyplan_discipline', 'Discente Disciplina')
    classe_teacher_discipline = fields.One2Many('akademy_classe.classe.teacher.discipline', 
        'studyplan_discipline', 'Docente Disciplina')
    classe_teacher_lesson = fields.One2Many('akademy_classe.classe.teacher.lesson', 
        'studyplan_discipline', 'Plano de aula')

    @classmethod
    def __setup__(cls):
        super(StudyPlanDiscipline, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('hours', Check(table, table.hours >= 1),
            u'Não foi possível cadastrar a disciplina neste plano de estudo, por favor verifica a carga horária.'),
            ('average', Check(table, table.average <= 20),
            u'Não foi possível cadastrar a disciplina neste plano de estudo, por favor verificar se a média de aprovação esta acima de 20 valores.')
        ]
        cls._order = [('discipline.name', 'ASC')]

    '''
    @classmethod
    def delete(cls, studyplan_disciplines):
        for studyplan_discipline in studyplan_disciplines:            
            if len(studyplan_discipline.studyplan.classes) < 1:
                super(StudyPlanDiscipline, cls).delete(studyplan_discipline)
            else:
                raise UserError("Não foi possível eliminar a discplina do plano de estudo, por favor verificar se o mesmo já tem uma turma associada.")	
    '''
    
    def get_rec_name(self, name):
        t1 = '%s' % \
            (self.discipline.rec_name)
        return t1

    @classmethod
    def search_rec_name(cls, name, clause):
        return [('discipline.rec_name',) + tuple(clause[1:])]


class StudyPlanAvaliation(ModelSQL, ModelView):
    'StudyPlan Avaliation'
    __name__ = 'akademy_configuration.studyplan.avaliation'
    
    description = fields.Text('Descrição') 
    perct_arithmetic = fields.Boolean(
        'Aritmética',
        depends=['perct_weighted'], 
        states={
            'invisible': Bool(Eval('perct_weighted')),
            'required': Not(Bool(Eval('perct_weighted')))
        },
        help="Calcula a média com base na operação aritmética.\n"+
        "Ex: Soma das avaliações, dividido pelo número de avaliações.")
    perct_weighted = fields.Boolean(
        'Ponderada',
        states={
            'invisible': Bool(Eval('perct_arithmetic')), 
            'required': Not(Bool(Eval('perct_arithmetic')))
        }, depends=['perct_arithmetic'], 
        help="Calcula a média com base na operação ponderada.\n"+
        "Ex: Soma da multiplicação das ponderações das avaliações, dividido pela soma das ponderações.")  
    percent = fields.Numeric(
        'Porcentagem', depends=['perct_weighted'],  
        states={
            'invisible': Not(Bool(Eval('perct_weighted'))), 
            'required': Bool(Eval('perct_weighted'))
        },
        help="A porcentagem varia entre 1%, a 100%.")  
    metric_avaliation = fields.Many2One('akademy_configuration.metric.avaliation', 'Avaliação',        
        required=True, help="Nome da Avaliação.", ondelete="RESTRICT")
    quarter = fields.Many2One('akademy_configuration.quarter', 
        'Período letivo', required=True, ondelete="RESTRICT", 
        help="Escolha o período letivo em que a avaliação será lecionada.")
    studyplan_discipline = fields.Many2One('akademy_configuration.studyplan.discipline', 
        'Disciplina') 
    state = fields.Many2One('akademy_configuration.discipline.state', 'Estado', 
        required=True, help="Escolha o estado de frequência.")

    @classmethod
    def __setup__(cls):
        super(StudyPlanAvaliation, cls).__setup__()  
        table = cls.__table__()
        cls._sql_constraints = [
            ('key', Unique(table, table.studyplan_discipline, table.quarter, table.metric_avaliation),
             u'Não foi possível cadastrar a nova avaliação, por favor verificar se a disciplina e o período letivo, já esixtem para está avaliação.')
        ]      
        cls._order = [('quarter.name', 'ASC')]

    '''
    @classmethod
    def delete(cls, studyplan_avaliations):
        for studyplan_avaliation in studyplan_avaliations:            
            if len(studyplan_avaliation.studyplan_discipline.studyplan.classes) < 1:
                super(StudyPlanAvaliation, cls).delete(studyplan_avaliations)
            else:
                raise UserError("Não foi possível eliminar avaliação da discplina por favor verificar se o plano de estudo já tem uma turma associada.")	
    '''
    
    def get_rec_name(self, name):
        t1 = '%s' % \
            (self.metric_avaliation.rec_name)
        return t1

    @classmethod
    def search_rec_name(cls, name, clause):
        return [('metric_avaliation.rec_name',) + tuple(clause[1:])] 


