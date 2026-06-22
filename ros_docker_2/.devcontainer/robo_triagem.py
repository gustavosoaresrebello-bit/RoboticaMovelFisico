#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import actionlib
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# ==========================================
# MAPEAMENTO DE COORDENADAS (Calibre depois!)
# ==========================================
X_BASE, Y_BASE = -9.17, 5.66  # Área de Carga (Onde o robô espera)

LOCAIS_DE_ARMAZENAMENTO = {
    'vermelho': (1.5, 1.95),   # Coordenada da prateleira vermelha
    'azul': (2.46, 0.32),      # Coordenada da prateleira azul
    'verde': (3.34, -1.2)      # Coordenada da prateleira verde
}

cliente_move_base = None

def enviar_objetivo(x, y):
    """Função que envia o robô para uma coordenada"""
    objetivo = MoveBaseGoal()
    objetivo.target_pose.header.frame_id = "map"
    objetivo.target_pose.header.stamp = rospy.Time.now()
    objetivo.target_pose.pose.position.x = x
    objetivo.target_pose.pose.position.y = y
    objetivo.target_pose.pose.orientation.w = 1.0
    
    cliente_move_base.send_goal(objetivo)
    cliente_move_base.wait_for_result()

def ao_receber_cor(mensagem):
    """Callback: Essa função dispara automaticamente quando o robô escuta uma cor nova"""
    cor = mensagem.data
    rospy.loginfo(f"\n[COMANDO RECEBIDO] Caixa da cor {cor.upper()} detectada!")
    
    if cor in LOCAIS_DE_ARMAZENAMENTO:
        x_destino, y_destino = LOCAIS_DE_ARMAZENAMENTO[cor]
        
        # 1. Vai até a prateleira da cor escolhida
        rospy.loginfo(f"Indo para o setor de itens da cor {cor}...")
        enviar_objetivo(x_destino, y_destino)
        
        # 2. Simula o robô guardando o item
        rospy.loginfo("[CHEGOU] Guardando o item nas prateleiras...")
        rospy.sleep(5.0)
        
        # 3. Volta para a base para buscar mais caixas
        rospy.loginfo("Trabalho concluído! Retornando para a Área de Carga...")
        enviar_objetivo(X_BASE, Y_BASE)
        rospy.loginfo("[BASE] Aguardando a próxima caixa na esteira...")
        
    else:
        rospy.logwarn("Erro de sistema: Local de armazenamento não encontrado.")

def iniciar_robo():
    global cliente_move_base
    rospy.init_node('cerebro_robo_triagem')
    
    # Conecta com a navegação
    cliente_move_base = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("Aguardando o Move Base...")
    cliente_move_base.wait_for_server()
    
    # Manda o robô para a Área de Carga no início do turno
    rospy.loginfo("Iniciando turno! Indo para a Área de Carga base...")
    enviar_objetivo(X_BASE, Y_BASE)
    
    # Se inscreve (subscribe) no tópico de cores e fica ouvindo eternamente
    rospy.loginfo("=== PRONTO! Aguardando mensagens do sensor de triagem ===")
    rospy.Subscriber('/cor_do_item', String, ao_receber_cor)
    rospy.spin()  # Impede que o script desligue

if __name__ == '__main__':
    try:
        iniciar_robo()
    except rospy.ROSInterruptException:
        pass