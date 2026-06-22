#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def enviar_objetivo(x, y):
    """Função que envia o robô para uma coordenada X, Y específica"""
    # Se conecta com o cérebro de navegação do robô
    cliente = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    
    rospy.loginfo("Aguardando conexão com o servidor move_base...")
    cliente.wait_for_server()
    
    # Cria o objeto de objetivo baseado no mapa estático (map)
    objetivo = MoveBaseGoal()
    objetivo.target_pose.header.frame_id = "map"
    objetivo.target_pose.header.stamp = rospy.Time.now()
    
    # Define a posição X e Y
    objetivo.target_pose.pose.position.x = x
    objetivo.target_pose.pose.position.y = y
    
    # Define a rotação (orientação padrão olhando para frente)
    objetivo.target_pose.pose.orientation.w = 1.0
    
    rospy.loginfo(f"Enviando robô para as coordenadas -> X: {x}, Y: {y}")
    cliente.send_goal(objetivo)
    
    # Espera até o robô chegar fisicamente no ponto
    cliente.wait_for_result()
    return cliente.get_state()

def loop_industrial():
    # Inicializa o nó do ROS para este script
    rospy.init_node('script_rotina_logistica')
    
    # Definição das coordenadas que você escolheu!
    X_CARGA, Y_CARGA = -9.17, 5.66
    X_DESCARGA, Y_DESCARGA = 0.0, 0.0
    
    rospy.loginfo("=== ROTINA DE LOGÍSTICA AUTÔNOMA INICIADA ===")
    
    ciclo = 1
    while not rospy.is_shutdown():
        rospy.loginfo(f"\n--- INICIANDO CICLO NÚMERO {ciclo} ---")
        
        # ----------------------------------------------------
        # ETAPA 1: IR PARA A ÁREA DE CARGA
        # ----------------------------------------------------
        rospy.loginfo("Movendo em direção à Área de Carga...")
        enviar_objetivo(X_CARGA, Y_CARGA)
        
        rospy.loginfo("[CHEGOU] Aguardando o carregamento dos itens simulados...")
        # Simula o robô parado coletando a caixa (Espera 7 segundos)
        rospy.sleep(7.0)
        rospy.loginfo("Carga concluída com sucesso!")
        
        # ----------------------------------------------------
        # ETAPA 2: IR PARA A ÁREA DE DESCARGA
        # ----------------------------------------------------
        rospy.loginfo("Movendo em direção à Área de Descarga...")
        enviar_objetivo(X_DESCARGA, Y_DESCARGA)
        
        rospy.loginfo("[CHEGOU] Descarregando e organizando os itens nas prateleiras...")
        # Simula o robô descarregando (Espera 7 segundos)
        rospy.sleep(7.0)
        rospy.loginfo("Descarga concluída!")
        
        ciclo += 1

if __name__ == '__main__':
    try:
        loop_industrial()
    except rospy.ROSInterruptException:
        rospy.loginfo("Rotina encerrada pelo usuário.")