''' test cloudAMQP_client '''  # pylint: disable=invalid-name
from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = 'amqp://lzpuqoey:N-sEnt68aQ9dUTs5f1cR047h12DO17GJ@donkey.rmq.cloudamqp.com/lzpuqoey'
TEST_QUEUE_NAME = 'test'


def test_basic():
    ''' test cloudAMQP_client '''
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

    sent_msg = {'test': 'test'}
    client.send_message(sent_msg)
    received_msg = client.get_message()

    assert sent_msg == received_msg
    print 'test_basic passed.'


if __name__ == '__main__':
    test_basic()
