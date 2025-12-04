# This file is part of SAGE Education.   The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import Pool, PoolMeta


class Employee(metaclass=PoolMeta):
    'Employee'
    __name__ = 'company.employee'
       
    classe_treacher = fields.One2Many('akademy_classe.classe.teacher', 
        'employee', 'Associar turma')


class Student(metaclass=PoolMeta):
    'Student'
    __name__ = 'company.student'
       
    classe = fields.Many2One('akademy_configuration.classe', 'Classe', 
        domain=[('course_classe.course', '=', Eval('course', -1))],
        depends=['course'], help="Nome da classe.")
    academic_level = fields.Many2One('akademy_configuration.academic.level', 
        'Nível académico', required=True)
    area = fields.Many2One('akademy_configuration.area', 'Área',          
        domain=[
            ('academic_level', '=', Eval('academic_level', -1))
        ], depends=['academic_level'], required=True)
    course = fields.Many2One('akademy_configuration.course', 'Curso',          
        domain=[('area', '=', Eval('area', -1))], 
        depends=['area'], required=True)
    state = fields.Many2One('akademy_configuration.matriculation.state', 
        'Estado', help="Escolha o estado de matrícula.")
    classe_student = fields.One2Many('akademy_classe.classe.student', 
        'student', 'Matrículas')
    
    @classmethod
    def update_student(cls, student, classe, state):
        MatriculationState = Pool().get('akademy_configuration.matriculation.state')
        student.classe = classe 
        student.state = MatriculationState.search([('name', '=', state)])[0]
        student.save()

