import os
import random
import time
from flask import Flask


from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.resource import ResourceAttributes

app = Flask(__name__)

# Configuração do OpenTelemetry para Produção
tempo_endpoint = os.environ.get("TEMPO_ENDPOINT")
if not tempo_endpoint:
    raise RuntimeError("A variável de ambiente TEMPO_ENDPOINT é obrigatória.")

resource = Resource(attributes={ResourceAttributes.SERVICE_NAME: "servico-externo"})
trace.set_tracer_provider(TracerProvider(resource=resource))

otlp_exporter = OTLPSpanExporter(endpoint=tempo_endpoint, insecure=True)

trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
FlaskInstrumentor().instrument_app(app)

def random_sleep():
    sleep_time = random.uniform(0, 3)
    time.sleep(sleep_time)
    return sleep_time

@app.route("/externo")
def external():
    sleep_time = random_sleep()
    return f"Resposta do Serviço Externo após {sleep_time:.2f} segundos de espera."

if __name__ == "__main__":
    # Não use o servidor de desenvolvimento em produção
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
