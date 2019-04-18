CREATE TRIGGER update_all_recite_time
  AFTER update
  ON happy_recite_word_excelstatus
  FOR EACH ROW
  UPDATE happy_recite_word_words
  SET happy_recite_word_words.recite_time = NEW.recite_time
  WHERE happy_recite_word_words.file_source_id = NEW.id;

CREATE TRIGGER update_recite_time_then_update_recite_time
  AFTER UPDATE
  ON happy_recite_word_excelstatus
  FOR EACH ROW
  UPDATE happy_recite_word_words
  SET happy_recite_word_words.recite_count = happy_recite_word_words.recite_count + 1
  WHERE happy_recite_word_words.file_source_id = NEW.id;

SHOW TRIGGERS;