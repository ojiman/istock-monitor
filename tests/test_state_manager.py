import json
import pytest
from src import state_manager

def test_write_and_read_state(tmp_path, monkeypatch):
    """
    Tests the happy path: successfully writing a state dictionary to a file
    and then reading it back correctly.
    """
    # Create a temporary file path within the test-specific directory
    temp_state_file = tmp_path / "state.json"
    
    # Use monkeypatch to temporarily point the state_manager to our temp file
    monkeypatch.setattr(state_manager, "STATE_FILE", str(temp_state_file))
    
    # 1. Test the write_state function
    test_data = {"product1": ["storeA", "storeB"], "product2": []}
    state_manager.write_state(test_data)
    
    # Verify the file content directly
    with open(temp_state_file, 'r', encoding='utf-8') as f:
        content_on_disk = json.load(f)
        assert content_on_disk == test_data
        
    # 2. Test the read_state function
    read_data = state_manager.read_state()
    assert read_data == test_data

def test_read_state_file_not_found(tmp_path, monkeypatch):
    """
    Tests that read_state returns an empty dictionary when the state file
    does not exist.
    """
    non_existent_file = tmp_path / "non_existent_state.json"
    monkeypatch.setattr(state_manager, "STATE_FILE", str(non_existent_file))
    
    read_data = state_manager.read_state()
    assert read_data == {}

def test_read_state_empty_file(tmp_path, monkeypatch):
    """
    Tests that read_state returns an empty dictionary when the state file
    is completely empty.
    """
    empty_file = tmp_path / "empty_state.json"
    empty_file.touch()  # Create a zero-byte file
    monkeypatch.setattr(state_manager, "STATE_FILE", str(empty_file))
    
    read_data = state_manager.read_state()
    assert read_data == {}

def test_read_state_corrupted_json(tmp_path, monkeypatch):
    """
    Tests that read_state returns an empty dictionary when the state file
    contains malformed JSON.
    """
    corrupted_file = tmp_path / "corrupted_state.json"
    corrupted_file.write_text("this is not valid json", encoding='utf-8')
    monkeypatch.setattr(state_manager, "STATE_FILE", str(corrupted_file))
    
    read_data = state_manager.read_state()
    assert read_data == {}
