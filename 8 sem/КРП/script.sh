#!/bin/bash

# --- НАСТРОЙКИ ---
# Владелец ПРОЕКТА (тот, в чьем профиле находится доска Projects)
# Судя по скриншотам, это Никита. Если проект у Данилы - поменяйте обратно.
PROJECT_OWNER="nikitafilipenko2" 
PROJECT_NUM=4
REPO="nikitafilipenko2/RatingSiteKRP"
CSV_FILE="data.csv"

# Проверка наличия файла
if [ ! -f "$CSV_FILE" ]; then
    echo "Файл $CSV_FILE не найден!"
    exit 1
fi

echo "Файл найден. Начинаем импорт..."

# ВАЖНО: IFS=';' задает разделитель точку с запятой
# tr -d '\r' удаляет символы возврата каретки (проблема Windows)
while IFS=';' read -r title status type priority iteration || [ -n "$title" ]
do
  # Очистка переменных от лишних пробелов и символов Windows (\r)
  title=$(echo "$title" | tr -d '\r')
  status=$(echo "$status" | tr -d '\r')
  type=$(echo "$type" | tr -d '\r')
  priority=$(echo "$priority" | tr -d '\r')
  iteration=$(echo "$iteration" | tr -d '\r')

  # Пропуск пустых строк или строки заголовка (если она попала)
  if [ -z "$title" ] || [ "$title" == "Title" ]; then 
      continue 
  fi

  echo "------------------------------------------------"
  echo "Обработка: $title"

  # 1. Создаем Issue (убрали 2>/dev/null, чтобы видеть ошибки!)
  # Добавляем --label "$type", если такого лейбла нет в репо, будет предупреждение, но issue создастся.
  
  OUTPUT=$(gh issue create \
    --repo "$REPO" \
    --title "$title" \
    --body "Imported from Excel.
    
**Details:**
- **Original Status:** $status
- **Type:** $type
- **Priority:** $priority
- **Iteration:** $iteration" \
    --label "$type")

  # Если команда выполнилась успешно, в OUTPUT будет URL
  if [[ $OUTPUT == http* ]]; then
     echo " -> Issue создана: $OUTPUT"
     
     # 2. Добавляем в проект
     # Внимание: --owner должен быть владельцем проекта
     echo " -> Добавляю в проект #$PROJECT_NUM владельца $PROJECT_OWNER..."
     
     gh project item-add "$PROJECT_NUM" --owner "$PROJECT_OWNER" --url "$OUTPUT"
     
  else
     echo "ОШИБКА создания Issue:"
     echo "$OUTPUT"
  fi
  
  sleep 1

done < <(tail -n +2 "$CSV_FILE")

echo "------------------------------------------------"
echo "Готово!"