import streamlit as st
from collections import Counter
from typing import List, Dict, Any, Optional

class CasinoAnalyzer:
    def __init__(self, history: List[str]):
        self.results = history

    def analyze_micro_patterns(self) -> List[Dict[str, Any]]:
        patterns = []
        if len(self.results) < 6:
            return patterns
        
        last6 = self.results[-6:]
        double_pattern_count = sum(1 for i in range(0, 6, 2)
                                   if i + 1 < 6 and last6[i] == last6[i + 1] and last6[i] != 'E')

        if double_pattern_count >= 2:
            patterns.append({
                'type': 'micro_double_pattern',
                'strength': double_pattern_count / 3,
                'risk': 'critical' if double_pattern_count == 3 else 'high',
                'description': f'Padrão 2x2 repetitivo ({double_pattern_count}/3)',
                'manipulation': 'CRÍTICA - Sistema forçando padrão' if double_pattern_count == 3 else 'ALTA',
                'predictability': 85
            })

        last8_non_empate = [r for r in self.results if r != 'E'][-8:]
        if len(last8_non_empate) >= 6:
            micro_alternations = sum(1 for i in range(1, min(6, len(last8_non_empate)))
                                    if last8_non_empate[i] != last8_non_empate[i-1])
            if micro_alternations >= 4:
                patterns.append({
                    'type': 'micro_alternation',
                    'strength': micro_alternations / 5,
                    'risk': 'critical' if micro_alternations == 5 else 'high',
                    'description': f'Micro-alternação suspeita ({micro_alternations}/5)',
                    'manipulation': 'Sistema induzindo alternância artificial',
                    'predictability': 90
                })
        return patterns

    def detect_hidden_cycles(self) -> List[Dict[str, Any]]:
        patterns = []
        non_empate = [r for r in self.results if r != 'E']
        if len(non_empate) < 12:
            return patterns
        
        for cycle_size in range(3, 7):
            cycles = [''.join(non_empate[i:i+cycle_size]) for i in range(len(non_empate) - cycle_size + 1)]
            cycle_counts = Counter(cycles)
            repeated = [(cycle, count) for cycle, count in cycle_counts.items() if count >= 2]
            if repeated:
                most_repeated, count = max(repeated, key=lambda x: x[1])
                patterns.append({
                    'type': 'hidden_cycle',
                    'cycle_size': cycle_size,
                    'pattern': most_repeated,
                    'repetitions': count,
                    'strength': min(count / 3, 1),
                    'risk': 'high' if count >= 3 else 'medium',
                    'description': f'Ciclo oculto detectado: "{most_repeated}" ({count}x)',
                    'manipulation': 'Sistema usando ciclo programado' if count >= 3 else 'Possível ciclo induzido',
                    'predictability': 70 + (count * 5)
                })
        return patterns

    def analyze_compensation_patterns(self) -> List[Dict[str, Any]]:
        patterns = []
        non_empate = [r for r in self.results if r != 'E']
        n = len(non_empate)
        if n < 20:
            return patterns

        windows = [12, 15, 18]

        for window_size in windows:
            if n >= window_size:
                window = non_empate[-window_size:]
                c_count = window.count('C')
                v_count = window.count('V')
                imbalance = abs(c_count - v_count)
                balance_ratio = imbalance / window_size

                if balance_ratio < 0.1 and window_size >= 15:
                    patterns.append({
                        'type': 'artificial_balance',
                        'window_size': window_size,
                        'balance': f"{c_count}C/{v_count}V",
                        'strength': 1 - balance_ratio,
                        'risk': 'high',
                        'description': f'Equilíbrio artificial em {window_size} jogadas',
                        'manipulation': 'Sistema forçando distribuição 50/50',
                        'predictability': 85
                    })

                if balance_ratio > 0.4:
                    underrepresented = 'C' if c_count < v_count else 'V'
                    patterns.append({
                        'type': 'compensation_pending',
                        'window_size': window_size,
                        'imbalance': imbalance,
                        'favored_color': underrepresented,
                        'strength': balance_ratio,
                        'risk': 'medium',
                        'description': f'Compensação pendente: {c_count}C vs {v_count}V',
                        'manipulation': f'Sistema deve favorecer {underrepresented}',
                        'predictability': 60 + (balance_ratio * 20)
                    })
        return patterns

    def analyze_strategic_ties(self) -> List[Dict[str, Any]]:
        patterns = []
        results = self.results
        if len(results) < 8:
            return patterns
        tie_positions = [i for i, r in enumerate(results) if r == 'E']

        def get_sequence_length(seq):
            if not seq:
                return 0
            color = seq[-1]
            length = 1
            for i in range(len(seq)-2, -1, -1):
                if seq[i] == color:
                    length += 1
                else:
                    break
            return length

        for tie_pos in tie_positions:
            if tie_pos >= 3:
                before = results[max(0, tie_pos-3):tie_pos]
                after = results[tie_pos+1:tie_pos+4]

                if len(before) >= 2 and before[-1] == before[-2] and before[-1] != 'E':
                    patterns.append({
                        'type': 'strategic_tie_after_sequence',
                        'position': tie_pos,
                        'sequence_color': before[-1],
                        'sequence_length': get_sequence_length(before),
                        'strength': 0.7,
                        'risk': 'high',
                        'description': f'Empate estratégico após {get_sequence_length(before)}x {before[-1]}',
                        'manipulation': 'Empate usado para quebrar momentum',
                        'predictability': 75
                    })

                if len(after) >= 2 and len(before) >= 1 and before[-1] != 'E' and after[0] != 'E':
                    before_color = before[-1]
                    after_color = after[0]
                    if before_color != after_color:
                        patterns.append({
                            'type': 'strategic_tie_before_reversal',
                            'position': tie_pos,
                            'from_color': before_color,
                            'to_color': after_color,
                            'strength': 0.8,
                            'risk': 'high',
                            'description': f'Empate estratégico antes de reversão {before_color} → {after_color}',
                            'manipulation': 'Empate usado para mascarar mudança direcionada',
                            'predictability': 80
                        })

        return patterns

    def assess_risk(self, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        risk_score = 0
        risk_factors = []

        for pattern in patterns:
            if pattern['type'] == 'micro_double_pattern' and pattern['strength'] >= 0.8:
                risk_score += 70
                risk_factors.append('🚨 Padrão 2x2 crítico detectado')
            elif pattern['type'] == 'micro_alternation' and pattern['strength'] >= 0.8:
                risk_score += 65
                risk_factors.append('⚠️ Alternação artificial crítica')
            elif pattern['type'] == 'hidden_cycle' and pattern.get('repetitions', 0) >= 3:
                risk_score += 60
                risk_factors.append(f'🔄 Ciclo programado ativo ({pattern.get("repetitions")}x)')
            elif pattern['type'] == 'artificial_balance':
                risk_score += 55
                risk_factors.append('⚖️ Equilíbrio artificial forçado')
            elif pattern['type'] == 'intentional_break':
                risk_score += 50
                risk_factors.append('💥 Quebra intencional detectada')
            elif pattern['type'].startswith('strategic_tie'):
                risk_score += 40
                risk_factors.append('🔶 Empate estratégico detectado')

        if risk_score >= 80:
            level = 'critical'
        elif risk_score >= 55:
            level = 'high'
        elif risk_score >= 30:
            level = 'medium'
        else:
            level = 'low'

        return {'level': level, 'score': min(risk_score, 100), 'factors': risk_factors}

    def detect_manipulation(self, patterns: List[Dict[str, Any]], risk: Dict[str, Any]) -> Dict[str, Any]:
        manipulation_score = 0
        manipulation_signs = []

        for pattern in patterns:
            predictability = pattern.get('predictability', 0)
            if predictability >= 90:
                manipulation_score += 80
                manipulation_signs.append(f"🤖 Padrão altamente artificial: {pattern['description']}")
            elif predictability >= 80:
                manipulation_score += 60
                manipulation_signs.append(f"🎯 Padrão programado: {pattern['description']}")
            elif predictability >= 70:
                manipulation_score += 40
                manipulation_signs.append(f"⚙️ Padrão suspeito: {pattern['description']}")

        level = 'low'
        if manipulation_score >= 80:
            level = 'critical'
        elif manipulation_score >= 60:
            level = 'high'
        elif manipulation_score >= 35:
            level = 'medium'

        return {'level': level, 'score': min(manipulation_score, 100), 'signs': manipulation_signs}

    def make_prediction(self, patterns: List[Dict[str, Any]], risk: Dict[str, Any], manipulation: Dict[str, Any]) -> Dict[str, Any]:
        prediction = {'color': None, 'confidence': 0, 'reasoning': '', 'strategy': 'AGUARDAR MELHORES CONDIÇÕES'}

        if risk['level'] == 'critical' or manipulation['level'] == 'critical':
            prediction['reasoning'] = '🚨 CONDIÇÕES CRÍTICAS - Manipulação máxima detectada'
            prediction['strategy'] = 'PARAR COMPLETAMENTE'
            return prediction

        if manipulation['level'] == 'high':
            prediction['reasoning'] = '⛔ Manipulação alta - Evitar apostas'
            prediction['strategy'] = 'AGUARDAR NORMALIZAÇÃO'
            return prediction

        compensation_pattern = next((p for p in patterns if p['type'] == 'compensation_pending'), None)
        if compensation_pattern and risk['level'] == 'low' and manipulation['level'] == 'low':
            color = compensation_pattern['favored_color']
            confidence = min(75, 55 + (compensation_pattern['strength'] * 20))
            prediction.update({
                'color': color,
                'confidence': confidence,
                'reasoning': f'Compensação estatística esperada: {compensation_pattern["description"]}',
                'strategy': 'APOSTAR COMPENSAÇÃO'
            })
            return prediction

        cycle_pattern = next((p for p in patterns if p['type'] == 'hidden_cycle' and p.get('repetitions', 0) >= 2), None)
        if cycle_pattern and risk['level'] == 'low' and manipulation['level'] == 'low':
            next_color = self.predict_next_in_cycle(cycle_pattern['pattern'])
            if next_color:
                prediction.update({
                    'color': next_color,
                    'confidence': min(70, 50 + (cycle_pattern['repetitions'] * 5)),
                    'reasoning': f'Ciclo detectado: "{cycle_pattern["pattern"]}" ({cycle_pattern["repetitions"]}x)',
                    'strategy': 'SEGUIR CICLO'
                })
                return prediction

        non_empate = [r for r in self.results if r != 'E']
        if not non_empate:
            return prediction
        counter = Counter(non_empate)
        most_common_color, count = counter.most_common(1)[0]
        confidence = (count / len(non_empate)) * 100

        prediction.update({
            'color': most_common_color,
            'confidence': min(confidence, 75),
            'reasoning': f'Aposta baseada em frequência histórica de "{most_common_color}" ({count}/{len(non_empate)})',
            'strategy': 'APOSTAR NA PRINCIPAL COR'
        })
        return prediction

    def predict_next_in_cycle(self, pattern: str) -> Optional[str]:
        non_empate = [r for r in self.results if r != 'E']
        if not pattern or not non_empate:
            return None
        cycle_len = len(pattern)
        for i in range(len(non_empate)):
            expected = pattern[i % cycle_len]
            if non_empate[i] != expected:
                break
        pos = len(non_empate) % cycle_len
        return pattern[pos] if pos < cycle_len else None


def main():
    st.title("Casino Analyzer - Insira os Resultados Rapidamente")

    # Histórico persistente na sessão
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Botões dinâmicos coloridos para inserir resultados rapidamente
    col_c, col_v, col_e = st.columns(3)

    if col_c.button("C (Jogador)", key="btn_c"):
        st.session_state.history.append('C')
    if col_v.button("V (Banqueiro)", key="btn_v"):
        st.session_state.history.append('V')
    if col_e.button("E (Empate)", key="btn_e"):
        st.session_state.history.append('E')

    # Botões para limpar e apagar último resultado
    col_clear, col_undo, _ = st.columns([2, 2, 1])
    if col_clear.button("Limpar Histórico"):
        st.session_state.history = []
    if col_undo.button("Apagar Último Resultado"):
        if st.session_state.history:
            st.session_state.history.pop()

    # Exibição do histórico invertido com cores (mais recente à esquerda)
    if st.session_state.history:
        st.write("### Histórico Atual (Mais recente à esquerda):")
        color_map = {'C': '🟦', 'V': '🟥', 'E': '🟨'}
        history_display = ' '.join(color_map.get(r, '⬜') + r for r in reversed(st.session_state.history))
        st.markdown(history_display)
    else:
        st.info("Clique nos botões acima para inserir resultados e iniciar a análise.")
        return

    analyzer = CasinoAnalyzer(st.session_state.history)

    with st.spinner('Analisando dados...'):
        micro_patterns = analyzer.analyze_micro_patterns()
        hidden_cycles = analyzer.detect_hidden_cycles()
        compensation_patterns = analyzer.analyze_compensation_patterns()
        strategic_ties = analyzer.analyze_strategic_ties()

        patterns = micro_patterns + hidden_cycles + compensation_patterns + strategic_ties

        risk = analyzer.assess_risk(patterns)
        manipulation = analyzer.detect_manipulation(patterns, risk)
        prediction = analyzer.make_prediction(patterns, risk, manipulation)

    st.header("Padrões Detectados")
    if patterns:
        for p in patterns:
            st.write(f"- {p['description']} (Tipo: {p['type']}, Risco: {p['risk']})")
    else:
        st.write("Nenhum padrão significativo detectado.")

    st.header("Avaliação de Risco")
    st.write(f"Nível: **{risk['level'].upper()}** - Score: {risk['score']}")
    if risk['factors']:
        for f in risk['factors']:
            st.write(f"- {f}")

    st.header("Avaliação de Manipulação")
    st.write(f"Nível: **{manipulation['level'].upper()}** - Score: {manipulation['score']}")
    if manipulation['signs']:
        for s in manipulation['signs']:
            st.write(f"- {s}")

    st.header("Predição")
    if prediction['color']:
        st.write(f"Aposta sugerida: **{prediction['color']}**")
        st.write(f"Confiança: **{prediction['confidence']:.1f}%**")
        st.write(f"Razão: {prediction['reasoning']}")
        st.write(f"Estratégia: {prediction['strategy']}")
    else:
        st.write("Sem predição confiável disponível no momento.")
        st.write(prediction['reasoning'])

if __name__ == "__main__":
    main()
