from fastapi import FastAPI, HTTPException

from app.phone import Phone, CreatePhoneModel
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

phones: list[Phone] = [
    # Phone(0, 'Amazon Fire Phone', 'Amazon')
    # Phone(1, 'Asus PadFone', 'Asus'),
    # Phone(2, 'BlackBerry Priv', 'BlackBerry Limited'),
    # Phone(3, 'HTC Dream', 'HTC'),
    # Phone(4, 'Honor 9', 'Huawei')
]


def add_phones(content: CreatePhoneModel):
    id = len(phones)
    phones.append(Phone(id, content.model, content.developer))
    return id


app = FastAPI()

###############
# Jaeger

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource(attributes={
    SERVICE_NAME: "phones-service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

#
###############

###############
# Prometheus

from prometheus_fastapi_instrumentator import Instrumentator


@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

#
###############


@app.get("/v1/phones")
async def get_phones():
    return phones


@app.post("/v1/phones")
async def add_phone(content: CreatePhoneModel):
    add_phones(content)
    return phones[-1]


@app.get("/v1/phones/{id}")
async def get_phone_by_id(id: int):
    result = [item for item in phones if item.id == id]
    if len(result) > 0:
        return result[0]
    raise HTTPException(status_code=404, detail="Phone not found")


@app.get("/__health")
async def check_service():
    return
