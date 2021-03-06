import mock
import docker
import pytest

from sdk import coreapi, models

from runner import settings
from runner.processors import DockerProcessor
from runner import exceptions
from runner import settings

mockery = {
    "event": models.Event(name='event'),
    "operation": {
        "container": "container",
        "processId": "process_id",
        "systemId": "system_id",
        "image":"image",
        "processInstanceId":"id",
        "id":"id"
    },
    "process_instance": {
        "id": "instance_id",
    },
    "operation_instance": {
        "container": "container",
        "processId": "process_id",
        "systemId": "system_id",
        "image":"container",
        "processInstanceId":"instance_id",
        "id":"id"
    }
}


@mock.patch('docker.client.ContainerCollection')
@mock.patch('sdk.coreapi.get_operation_by_event')
@mock.patch('sdk.process_memory.create_memory')
@mock.patch('sdk.coreapi.create_process_instance')
@mock.patch('sdk.coreapi.create_operation_instance')
def test_execute_creates_process_instance(mock_create_process_instance,
                                          mock_create_process_memory,
                                          mock_get_operation_by_event,
                                          mock_containers,
                                          mock_create_operation_instance):
    docker_processor = DockerProcessor()
    mock_get_operation_by_event.return_value = mockery["operation"]
    mock_create_process_instance.return_value = None
    mock_create_operation_instance.return_value = mockery["operation_instance"]
    # act
    docker_processor.process(mockery["event"])

    # assert
    mock_create_process_instance.assert_called()
    mock_create_process_memory.assert_called()

@mock.patch('docker.client.ContainerCollection')
@mock.patch('sdk.coreapi.get_operation_by_event')
@mock.patch('sdk.process_memory.create_memory')
@mock.patch('sdk.coreapi.create_process_instance')
@mock.patch('sdk.coreapi.create_operation_instance')
def test_execute_creates_process_instance_invalid_event(mock_create_operation_instance,
                                          mock_create_process_instance,
                                          mock_create_process_memory,
                                          mock_get_operation_by_event,
                                          mock_containers):
    docker_processor = DockerProcessor()
    mock_get_operation_by_event.return_value = None
    mock_create_process_instance.return_value = None
    mock_create_operation_instance.return_value = None
    # act
    docker_processor.process(models.Event(name=''))

    # assert
    mock_create_process_instance.assert_not_called()
    mock_create_process_memory.assert_not_called()


@mock.patch('docker.client.ContainerCollection')
@mock.patch('sdk.coreapi.get_operation_by_event')
@mock.patch('sdk.process_memory.create_memory')
@mock.patch('sdk.coreapi.create_process_instance')
@mock.patch('sdk.coreapi.create_operation_instance')
def test_execute_creates_process_memory(mock_create_operation_instance,
                                        mock_create_process_instance,
                                        mock_create_process_memory,
                                        mock_get_operation_by_event,
                                        mock_containers):
    docker_processor = DockerProcessor()
    mock_get_operation_by_event.return_value = mockery["operation"]
    mock_create_process_instance.return_value = mockery["process_instance"]
    mock_create_operation_instance.return_value = mockery["operation_instance"]

    # act
    docker_processor.process(mockery["event"])
    # assert
    mock_create_process_instance.assert_called_with(mockery["operation"],mockery["event"].name)
    mock_create_process_memory.assert_called_with(
        mockery["process_instance"], mockery["event"])


@mock.patch('docker.client.ContainerCollection')
@mock.patch('sdk.coreapi.get_operation_by_event')
@mock.patch('sdk.process_memory.create_memory')
@mock.patch('sdk.coreapi.create_process_instance')
@mock.patch('sdk.coreapi.create_operation_instance')
def test_execute_new_instance(mock_create_operation_instance,
                              mock_create_process_instance,
                              mock_create_process_memory,
                              mock_get_operation_by_event,
                              mock_containers):
    # mock
    docker_processor = DockerProcessor()

    mock_get_operation_by_event.return_value = mockery["operation"]
    mock_create_process_instance.return_value = mockery["process_instance"]
    mock_create_operation_instance.return_value = mockery["operation_instance"]

    # act
    docker_processor.process(mockery["event"])

    # assert
    docker_processor.client.containers.run.assert_called()
